from fastapi.testclient import TestClient

from app import app
from app.database import init_db


init_db()


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "PocketSmart AI" in response.text


def test_api_requires_login():

    response = client.post(
        "/api/generate-home",
        json={
            "budget": 10000,
            "rooms": [
                "Bedroom"
            ],
            "style": "modern",
            "notes": "",
        },
    )

    assert response.status_code == 401