from fastapi.testclient import TestClient
from app.main import app
from app.config import RATE_LIMIT
from app.rate_limiter import rate_limiter

client = TestClient(app)


def test_end_to_end_rate_limit():
    rate_limiter.requests.clear()

    # Limit altı istekler
    for _ in range(RATE_LIMIT):
        response = client.get("/limited-endpoint")
        assert response.status_code == 200

    # Limit aşımı
    response = client.get("/limited-endpoint")
    assert response.status_code == 429
