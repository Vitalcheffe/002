import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_content():
    test_data = {
        "content": "Test content",
        "type": "summary",
        "language": "fr"
    }
    response = client.post("/analyze", json=test_data)
    assert response.status_code == 200 