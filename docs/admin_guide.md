# Administrator Guide

## Deployment Requirements
- Docker and Docker Compose
- Minimum 4GB RAM (to load the spaCy NLP model and NetworkX graph)
- Operating System: Linux/macOS/Windows (via WSL2)

## One-Command Startup
To start the entire application stack (FastAPI Backend + Streamlit UI):
```bash
docker-compose up --build -d
```
- API will be available at: `http://localhost:8000/docs` (Swagger UI)
- Streamlit Analyst UI will be available at: `http://localhost:8501`

## Directory Structure & Volumes
- `./logs`: Contains `api_audit.log` capturing every algorithmic decision, alert generated, and analyst action.
- `./mlruns`: Contains the MLflow tracking data (F1 scores, precision).
- `./data`: The generated synthetic supply chain topology.

## Security & Secrets
- Currently, the API uses a mocked token (`mock-analyst-token-123`). 
- In production, replace `security = HTTPBearer()` in `api/main.py` with an OAuth2 provider (e.g., Auth0, AWS Cognito) and inject via `.env`.
