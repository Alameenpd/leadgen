from fastapi.testclient import TestClient
from app.main import app
from app.services.lead_scraper_service import lead_scraper
import pytest

@pytest.fixture(autouse=True)
def mock_lead_scraper(monkeypatch):
    async def mock_scrape_linkedin(*args, **kwargs):
        return [
            {"name": "Test Lead", "email": "testlead@example.com", "linkedin_url": "https://linkedin.com/in/testlead"}
        ]
    monkeypatch.setattr(lead_scraper, "scrape_linkedin", mock_scrape_linkedin)

def test_scrape_linkedin_leads(client: TestClient, mock_lead_scraper):
    # First register and login a user
    client.post("/auth/register", json={"email": "test@example.com", "password": "testpassword"})
    login_response = client.post("/auth/token", data={"username": "test@example.com", "password": "testpassword"})
    access_token = login_response.json()["access_token"]

    # Then try to scrape leads
    response = client.post("/leads/scrape-linkedin", 
                           json={"search_query": "software engineer", "max_results": 1},
                           headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert "message" in response.json()