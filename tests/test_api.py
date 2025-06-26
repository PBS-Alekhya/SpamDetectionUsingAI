# tests/test_api.py
#  date : 9th june 2025
from fastapi.testclient import TestClient  
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Spam Detection API"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_spam():
    response = client.post("/predict", json={"post": "Free recharge, click here!"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert "confidence" in response.json()

def test_predict_not_spam():
    response = client.post("/predict", json={"post": "Hello, how are you?"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert "confidence" in response.json()
