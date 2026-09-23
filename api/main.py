import logging
import datetime
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional

# Import our previous modules
from ingestion.filter import is_relevant, is_english
from nlp.extract import BaselineExtractor
from graph.engine import SupplyChainGraph
from scoring.score import ScoringEngine

# Setup basic audit logging
import os
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/api_audit.log", 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="News-to-Risk Early Warning API",
    description="FastAPI Backend for Supply Chain Alerts"
)

# Mock Authentication
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if token != "mock-analyst-token-123":
        logging.warning(f"AUTH FAILED: Attempted access with token: {token}")
        raise HTTPException(status_code=403, detail="Invalid analyst token")
    return "analyst_user"

# Initialize singletons for Graph and Extractor
extractor = BaselineExtractor()
graph_engine = SupplyChainGraph()
# Try loading graph data; if running from tests, path might differ, handled gracefully
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
try:
    graph_engine.load_from_csv(data_dir)
except Exception as e:
    logging.error(f"Failed to load graph data: {e}")
scoring_engine = ScoringEngine(graph_engine, "logs")

# In-Memory DB
DB_ALERTS = {}

# --- Pydantic Schemas ---
class NewsIngestRequest(BaseModel):
    source_url: str
    published_date: str
    raw_text: str

class AlertResponse(BaseModel):
    alert_id: str
    event_id: str
    affected_supplier_id: str
    affected_product_id: str
    exposure_score: float
    explanation: str
    status: str

class FeedbackRequest(BaseModel):
    action: str = Field(..., description="accept, reject, or re_rank")
    comments: Optional[str] = None

# --- Endpoints ---
@app.post("/api/v1/ingest", tags=["Ingestion"])
def ingest_news(payload: NewsIngestRequest):
    logging.info(f"INGEST: Received news from {payload.source_url}")
    
    # 1. Filter
    if not (is_english(payload.raw_text) and is_relevant(payload.raw_text)):
        logging.info("INGEST: Dropped due to filtering.")
        return {"status": "dropped", "reason": "Irrelevant or non-English"}
        
    # 2. Extract
    extracted = extractor.extract(payload.raw_text)
    event_dict = {
        "id": str(uuid4())[:8],
        "event_type": extracted["event_type"],
        "locs": extracted["locs"]
    }
    
    # 3. Score & Graph Link
    alerts = scoring_engine.process_event(event_dict)
    
    # 4. Save to DB
    alert_ids = []
    for a in alerts:
        a_id = str(uuid4())[:8]
        a["alert_id"] = a_id
        a["status"] = "pending"
        DB_ALERTS[a_id] = a
        alert_ids.append(a_id)
        
    logging.info(f"INGEST: Generated {len(alerts)} alerts for event {event_dict['id']}")
    return {"event_id": event_dict["id"], "alerts_generated": len(alerts), "alert_ids": alert_ids}

@app.get("/api/v1/alerts", response_model=List[AlertResponse], tags=["Alerts"])
def get_alerts():
    # Return ranked alerts (highest exposure first)
    sorted_alerts = sorted(DB_ALERTS.values(), key=lambda x: x["exposure_score"], reverse=True)
    logging.info(f"ALERTS GET: Returned {len(sorted_alerts)} alerts")
    return sorted_alerts

@app.post("/api/v1/alerts/{alert_id}/feedback", tags=["Analyst"])
def submit_feedback(alert_id: str, payload: FeedbackRequest, user: str = Depends(verify_token)):
    if alert_id not in DB_ALERTS:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    if payload.action not in ["accept", "reject", "re_rank"]:
        raise HTTPException(status_code=400, detail="Invalid action")
        
    # Update state
    DB_ALERTS[alert_id]["status"] = payload.action
    
    logging.info(f"FEEDBACK: Analyst '{user}' marked alert {alert_id} as {payload.action}. Comments: {payload.comments}")
    return {"status": "Feedback recorded", "alert_id": alert_id, "new_state": payload.action}
