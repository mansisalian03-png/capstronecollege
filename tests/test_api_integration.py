import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app, DB_ALERTS

client = TestClient(app)

def test_full_pipeline_integration():
    # 1. Clear In-Memory DB
    DB_ALERTS.clear()
    
    # 2. Ingest an irrelevant event (should be dropped)
    irrelevant_payload = {
        "source_url": "http://test.com",
        "published_date": "2023-10-01T00:00:00Z",
        "raw_text": "The company released its quarterly earnings report."
    }
    resp1 = client.post("/api/v1/ingest", json=irrelevant_payload)
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "dropped"
    
    # 3. Ingest a highly relevant event that targets our graph (Kaohsiung)
    relevant_payload = {
        "source_url": "http://test.com",
        "published_date": "2023-10-02T00:00:00Z",
        "raw_text": "A sudden walkout by dockworkers at the Port of Kaohsiung has paused unloading."
    }
    resp2 = client.post("/api/v1/ingest", json=relevant_payload)
    assert resp2.status_code == 200
    assert resp2.json()["alerts_generated"] > 0
    alert_ids = resp2.json()["alert_ids"]
    assert len(alert_ids) > 0
    
    # 4. Fetch Alerts to verify sorting and exposure scores
    resp3 = client.get("/api/v1/alerts")
    assert resp3.status_code == 200
    alerts = resp3.json()
    assert len(alerts) == len(alert_ids)
    
    # Verify the explainable path exists
    target_alert = alerts[0]
    assert "explanation" in target_alert
    assert "Kaohsiung" in target_alert["explanation"]
    assert target_alert["status"] == "pending"
    
    # 5. Analyst Feedback: Try without token (Should fail Auth)
    resp4 = client.post(f"/api/v1/alerts/{target_alert['alert_id']}/feedback", json={"action": "accept"})
    assert resp4.status_code == 401
    
    # 6. Analyst Feedback: Try with valid token
    headers = {"Authorization": "Bearer mock-analyst-token-123"}
    resp5 = client.post(f"/api/v1/alerts/{target_alert['alert_id']}/feedback", json={"action": "accept"}, headers=headers)
    assert resp5.status_code == 200
    
    # 7. Verify State updated
    resp6 = client.get("/api/v1/alerts")
    assert resp6.json()[0]["status"] == "accept"
    
    print("\n--- E2E Integration Test Passed ---")
    print(f"Generated Alert Explainable Path: {target_alert['explanation']}")
    print(f"Alert Status changed from pending to: {resp6.json()[0]['status']}")
