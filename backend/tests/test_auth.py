from fastapi.testclient import TestClient
from app.main import app

def test_register(client: TestClient):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login(client: TestClient):
    # First register a user
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    # Then try to login
    response = client.post("/auth/token", data={
        "username": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()