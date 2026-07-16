from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "HealthRisk API is running"}

def test_predict_endpoint():
    payload = {
        "age": 65,
        "gender": "M",
        "weight": 85.0,
        "bp": "140/90",
        "hr": 80,
        "smoker": "N"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "risk_probability" in data
    assert "high_risk" in data
    assert isinstance(data["high_risk"], bool)
