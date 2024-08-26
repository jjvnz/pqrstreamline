import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered, please check your email to verify your account"}

# Más tests para requests, autenticación, etc.
