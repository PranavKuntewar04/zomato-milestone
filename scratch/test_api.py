import os
import sys
import asyncio
from fastapi.testclient import TestClient

# Add project root to sys.path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app, lifespan

# We need to manually trigger lifespan for TestClient if we want the startup events
# However, TestClient supports `with TestClient(app) as client:` which triggers lifespan events.

def test_recommend_endpoint():
    print("Starting TestClient (this will trigger dataset loading via lifespan)...")
    with TestClient(app) as client:
        print("Sending POST request to /api/recommend...")
        payload = {
            "location": "delhi",
            "budget": "medium",
            "cuisine": "north indian",
            "min_rating": 4.0,
            "additional_prefs": "family-friendly"
        }
        response = client.post("/api/recommend", json=payload)
        
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("Summary:", data.get("summary"))
            print("Recommendations Count:", len(data.get("recommendations", [])))
            for rec in data.get("recommendations", []):
                print(f" - Rank {rec.get('rank')}: {rec.get('restaurant_name')}")
        else:
            print("Error:", response.text)

if __name__ == "__main__":
    test_recommend_endpoint()
