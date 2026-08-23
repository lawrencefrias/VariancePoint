from app.models import MortalityInput, RealitySimulationRequest, VarianceAssessmentRequest, VarianceState
from app.scoring import calculate_mortality_score, calculate_variance, simulate_reality


def test_mortality_score_stays_in_range():
    score = calculate_mortality_score(
        MortalityInput(
            technology_id="adfs",
            adoption_score=60,
            community_momentum_score=40,
            vendor_investment_score=35,
            talent_availability_score=50,
            migration_urgency_score=80,
        )
    )
    assert 0 <= score <= 100


def test_variance_score_zero_when_target_matches_current():
    assessment = calculate_variance(
        VarianceAssessmentRequest(
            current=VarianceState(platforms=["Entra", "Intune"]),
            target=VarianceState(platforms=["Entra", "Intune"]),
        )
    )
    assert assessment.variance_score == 0
    assert assessment.drift_score == 0


def test_reality_simulation_produces_three_branches():
    branches = simulate_reality(RealitySimulationRequest(users=5000, servers=600, technologies=["ADFS", "VMware"]))
    assert len(branches) == 3
    assert {b.branch_name for b in branches} == {"Branch A", "Branch B", "Branch C"}
