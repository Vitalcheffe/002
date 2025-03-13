import pytest
from fastapi.testclient import TestClient
from ..app.main import app
from ..app.database import get_db
from ..app.models import User

client = TestClient(app)

@pytest.fixture
def test_user():
    return User(
        id="test123",
        email="test@example.com",
        is_premium=True
    )

def test_analyze_content(test_user):
    response = client.post(
        "/api/analyze",
        json={
            "content": "Test content",
            "type": "summary"
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 200
    assert "result" in response.json() 