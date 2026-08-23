from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_variance_assessment_endpoint():
    payload = {
        "current": {"platforms": ["VMware", "ADFS", "SCCM"]},
        "target": {"platforms": ["Azure Native", "Entra", "Intune"]},
    }
    response = client.post("/api/v1/variance-assessments/calculate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "variance_score" in body
    assert "drift_score" in body
