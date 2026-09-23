# Threat Model

This document outlines the security and robustness threat model for the News-to-Risk Early Warning System.

## 1. Malformed or Malicious Input
**Threat**: The system scrapes external RSS feeds or APIs that might contain malformed characters, extreme lengths, or SQL injection vectors.
**Mitigation**: 
- Strict `Pydantic` schema validation on all entry points.
- ORM (SQLAlchemy/SQLModel) for database interactions to prevent SQLi.
- Text length truncation before NLP processing.

## 2. Spoofed or Poisoned Feeds
**Threat**: An attacker manipulates a monitored RSS feed to inject fake events (e.g., a fake factory fire) to manipulate risk scores and trigger false alerts.
**Mitigation**:
- Strict domain allow-listing for news sources.
- The analyst feedback loop acts as the human-in-the-loop defense (alerts are marked as `pending` until reviewed).
- Multi-source deduplication: an event requires mentions in at least 2 independent feeds to escalate severity.

## 3. PII and Sensitive Data Leakage
**Threat**: Unstructured news texts scraped from the web might contain Personally Identifiable Information (PII), which is then stored in our database.
**Mitigation**:
- The NLP pipeline specifically targets `ORG` (Organizations) and `GPE`/`LOC` (Locations). Any `PERSON` entities identified by spaCy are explicitly redacted or dropped before the event text is saved to the database.

## 4. Authentication and Authorization Bypass
**Threat**: Unauthorized users accessing the FastAPI backend to read proprietary exposure scores or poison the analyst feedback loop.
**Mitigation**:
- All FastAPI endpoints (except `/metrics` and `/health`) are secured behind a JWT-based Bearer token layer.
- Role-based Access Control (RBAC): Only tokens with the `analyst` claim can POST to the feedback endpoints.

## 5. Denial of Service via Duplicate Flooding
**Threat**: A single event generates 10,000 news articles, overwhelming the graph traversal and scoring engine.
**Mitigation**:
- **Deduplication Engine**: Runs *before* the graph engine. It uses TF-IDF/Cosine similarity on event text + location bounding to collapse duplicate events into a single node update.
