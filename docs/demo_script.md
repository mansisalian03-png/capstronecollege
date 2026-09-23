# Capstone Demo Recording Script

**Target Length**: 5 - 8 minutes
**Goal**: Demonstrate the end-to-end functionality, engineering rigor, and explainability of the system.

## Preparation Checklist
- [ ] Ensure Docker is running.
- [ ] Run `docker-compose up --build -d` to start the backend and UI.
- [ ] Open three terminal/browser tabs:
  1. Terminal showing the `logs/api_audit.log` (`tail -f logs/api_audit.log`)
  2. Browser with FastAPI Swagger UI (`http://localhost:8000/docs`)
  3. Browser with Streamlit UI (`http://localhost:8501`)

## Scene 1: Introduction & Architecture (1 min)
- **Show**: Your `architecture.md` Mermaid diagram (render it in VSCode).
- **Say**: "This is our Supply Chain Early Warning System. It ingests unstructured news, extracts entities using NLP, maps them to a NetworkX supply chain graph, and generates explainable exposure scores."

## Scene 2: The Data Layer & MLflow (1 min)
- **Show**: Briefly show `data/generate_graph.py` to prove the data is reproducible, not hardcoded.
- **Show**: Open `docs/evaluation.md` or the `mlruns/` UI.
- **Say**: "We tracked our NLP extraction F1 and Alert Precision using MLflow. Our NLP pipeline achieved an 82% alert precision, vastly outperforming our regex baseline."

## Scene 3: Ingestion & Extraction (2 mins)
- **Show**: Open the FastAPI Swagger UI (`http://localhost:8000/docs`). 
- **Action**: Use the `/ingest` POST endpoint. Submit this JSON:
  ```json
  {
    "source_url": "http://news.com",
    "published_date": "2023-10-02T00:00:00Z",
    "raw_text": "A sudden walkout by dockworkers at the Port of Los Angeles has paused unloading."
  }
  ```
- **Say**: "I am injecting a raw news event into the API. The Pydantic models validate the input. In the background, our spaCy model extracts 'Los Angeles' and the deduplication engine ensures we haven't processed this exact alert today. It then queries the NetworkX graph."

## Scene 4: Analyst UI & Explainability (2 mins)
- **Show**: Switch to the Streamlit UI (`http://localhost:8501`). Refresh the page.
- **Action**: Expand the newly generated alert.
- **Say**: "Our API just pushed this alert to the dashboard. The core innovation here is the *Explainable Path*. Notice how it doesn't just give a score; it tells the analyst exactly why: 'Strike event in Los Angeles -> Supplier operates in Los Angeles -> Product depends on Supplier'."

## Scene 5: Audit Trail & Security (1 min)
- **Action**: Click the "✅ Accept" button in the Streamlit UI.
- **Show**: Switch to the terminal running `tail -f logs/api_audit.log`.
- **Say**: "The analyst feedback loop requires a JWT Bearer token, ensuring RBAC security. Once I hit Accept, it logs the Human-in-the-Loop decision directly to our secure audit trail, which we can see here."

## Scene 6: Conclusion (30s)
- **Say**: "The system utilizes Docker, GitHub Actions CI, and comprehensive pytest coverage, achieving TRL-4 readiness for enterprise deployment."
