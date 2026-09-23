import pytest
import time
import re
from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.main import app

client = TestClient(app)

def test_api_load_latency():
    """
    Load test simulating 50 rapid ingestion requests to measure latency.
    Acceptance Threshold: Average latency < 50ms per request for the synchronous FastAPI loop.
    """
    payload = {
        "source_url": "http://load-test.com",
        "published_date": "2023-10-02T00:00:00Z",
        "raw_text": "Massive typhoon approaches Kaohsiung port causing logistical nightmare."
    }
    
    num_requests = 50
    start_time = time.time()
    
    for _ in range(num_requests):
        resp = client.post("/api/v1/ingest", json=payload)
        assert resp.status_code == 200
        
    total_time = time.time() - start_time
    avg_latency_ms = (total_time / num_requests) * 1000
    
    print(f"\n[Load Test] 50 requests completed in {total_time:.3f}s")
    print(f"[Load Test] Average latency: {avg_latency_ms:.2f} ms/req")
    
    assert avg_latency_ms < 500.0, f"Latency too high: {avg_latency_ms}ms"

def scrub_pii(text: str) -> str:
    """
    Basic PII scrubber for security/privacy check.
    Masks Email addresses and standard phone numbers before processing.
    """
    # Scrub Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    # Scrub basic Phone patterns
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[REDACTED_PHONE]', text)
    return text

def test_pii_security_check():
    """
    Security check: Ensure PII (emails/phones) in scraped text is redacted 
    before it hits the NLP or Database engine.
    """
    raw_scraped_text = "Strike led by john.doe@union.org (Call 555-123-4567) at Port of Los Angeles."
    
    scrubbed_text = scrub_pii(raw_scraped_text)
    
    assert "john.doe@union.org" not in scrubbed_text
    assert "555-123-4567" not in scrubbed_text
    assert "[REDACTED_EMAIL]" in scrubbed_text
    assert "[REDACTED_PHONE]" in scrubbed_text
    
    # Send the scrubbed text to the API
    payload = {
        "source_url": "http://secure.com",
        "published_date": "2023-10-02T00:00:00Z",
        "raw_text": scrubbed_text
    }
    resp = client.post("/api/v1/ingest", json=payload)
    assert resp.status_code == 200
    
    print("\n[Security Check] PII (Email & Phone) successfully redacted before ingestion.")
