from fastapi.testclient import TestClient
import pytest

from app import main as main_module
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


def test_mortality_weights_must_sum_to_one():
    payload = [
        {
            "technology_id": "adfs",
            "adoption_score": 20,
            "community_momentum_score": 20,
            "vendor_investment_score": 20,
            "talent_availability_score": 20,
            "migration_urgency_score": 20,
        }
    ]
    response = client.post(
        "/api/v1/mortality-index",
        json={
            "inputs": payload,
            "weights": {
                "adoption_weight": 0.3,
                "community_weight": 0.2,
                "vendor_weight": 0.2,
                "talent_weight": 0.2,
                "migration_weight": 0.2,
            },
        },
    )
    assert response.status_code == 422


def test_community_insight_not_appended_if_persist_fails():
    original_save = main_module._save_insights
    original_items = list(main_module.COMMUNITY_INSIGHTS)

    def _fail_save(_):
        raise RuntimeError("disk write failed")

    main_module._save_insights = _fail_save
    try:
        with pytest.raises(RuntimeError, match="disk write failed"):
            client.post(
                "/api/v1/community-insights",
                json={
                    "technology": "ADFS",
                    "expected_outcome": "Expected migration speed",
                    "actual_outcome": "Migration slowed by dependencies",
                    "would_repeat": False,
                    "migration_duration_months": 18,
                    "lessons_learned": "Map hidden dependencies earlier",
                },
            )
        assert list(main_module.COMMUNITY_INSIGHTS) == original_items
    finally:
        main_module._save_insights = original_save
