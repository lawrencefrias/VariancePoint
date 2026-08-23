from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .data import COMMUNITY_INSIGHTS, LIFECYCLE_EVENTS, MORTALITY_INPUTS, TECHNOLOGIES, _INSIGHTS_LOCK, _save_insights
from .models import (
    CommunityInsight,
    DashboardSummary,
    MortalityInput,
    MortalityWeights,
    RealitySimulationRequest,
    RealitySimulationResponse,
    RiskLevel,
    TechnologyMortality,
    VarianceAssessment,
    VarianceAssessmentRequest,
)
from .scoring import (
    build_debt_clock_entry,
    calculate_mortality_score,
    calculate_variance,
    risk_from_score,
    simulate_reality,
)

app = FastAPI(title="VariancePoint API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/technologies")
def list_technologies():
    return TECHNOLOGIES


@app.get("/api/v1/debt-clock")
def debt_clock():
    entries = []
    for event in LIFECYCLE_EVENTS:
        technology = next((t for t in TECHNOLOGIES if t.id == event.technology_id), None)
        if technology is None:
            continue
        entries.append(
            build_debt_clock_entry(
                technology_id=technology.id,
                technology_name=technology.name,
                deadline_type=event.event_type,
                deadline=event.event_date,
                migration_complexity="medium" if "extended" in event.event_type else "high",
                estimated_remediation_effort_days=90,
            )
        )
    return entries


@app.post("/api/v1/mortality-index", response_model=list[TechnologyMortality])
def mortality_index(inputs: list[MortalityInput], weights: MortalityWeights | None = None):
    output = []
    for row in inputs:
        score = calculate_mortality_score(row, weights)
        output.append(
            TechnologyMortality(
                technology_id=row.technology_id,
                mortality_score=score,
                risk_level=risk_from_score(score),
            )
        )
    return output


@app.post("/api/v1/variance-assessments/calculate", response_model=VarianceAssessment)
def variance_assessment(req: VarianceAssessmentRequest):
    return calculate_variance(req)


@app.post("/api/v1/reality-simulator/generate", response_model=RealitySimulationResponse)
def generate_reality(req: RealitySimulationRequest):
    return RealitySimulationResponse(branches=simulate_reality(req))


@app.get("/api/v1/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    debt_entries = debt_clock()
    mortality_exposure = len(
        [
            row
            for row in MORTALITY_INPUTS
            if risk_from_score(calculate_mortality_score(row)) in {RiskLevel.amber, RiskLevel.red}
        ]
    )

    return DashboardSummary(
        technology_health_score=68.4,
        debt_exposure_count=len([e for e in debt_entries if e.days_remaining < 730]),
        upcoming_deadlines=len([e for e in debt_entries if 0 <= e.days_remaining < 365]),
        mortality_exposure_count=mortality_exposure,
        budget_impact_forecast=2_450_000.0,
        top_risks=[
            "Legacy identity stack concentration",
            "Virtualization platform lock-in",
            "Deferred endpoint modernization",
        ],
    )


@app.get("/api/v1/community-insights")
def list_community_insights():
    return COMMUNITY_INSIGHTS


_MAX_INSIGHTS = 10_000


@app.post("/api/v1/community-insights", response_model=CommunityInsight)
def create_community_insight(payload: CommunityInsight):
    with _INSIGHTS_LOCK:
        if len(COMMUNITY_INSIGHTS) >= _MAX_INSIGHTS:
            raise HTTPException(status_code=429, detail="Submission quota reached")
        COMMUNITY_INSIGHTS.append(payload)
        _save_insights(COMMUNITY_INSIGHTS)
    return payload
