import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def get_health():
    """Get a response from health."""
    return client.get("/health")


def test_status_code(get_health):
    """Test status_code function."""
    assert get_health.status_code == 200
