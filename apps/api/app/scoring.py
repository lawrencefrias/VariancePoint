from __future__ import annotations

from datetime import date

from .models import (
    DebtClockEntry,
    MortalityInput,
    MortalityWeights,
    RealityBranch,
    RealitySimulationRequest,
    RiskLevel,
    VarianceAssessment,
    VarianceAssessmentRequest,
    VarianceBreakdown,
)


def risk_from_score(score: float) -> RiskLevel:
    if score < 40:
        return RiskLevel.green
    if score < 70:
        return RiskLevel.amber
    return RiskLevel.red


def calculate_mortality_score(inputs: MortalityInput, weights: MortalityWeights | None = None) -> float:
    w = weights or MortalityWeights()
    protective_score = (
        inputs.adoption_score * w.adoption_weight
        + inputs.community_momentum_score * w.community_weight
        + inputs.vendor_investment_score * w.vendor_weight
        + inputs.talent_availability_score * w.talent_weight
    )
    urgency_penalty = inputs.migration_urgency_score * w.migration_weight
    raw = max(0.0, min(100.0, 100 - protective_score + urgency_penalty))
    return round(raw, 2)


def build_debt_clock_entry(
    technology_id: str,
    technology_name: str,
    deadline_type: str,
    deadline: date,
    migration_complexity: str,
    estimated_remediation_effort_days: int,
) -> DebtClockEntry:
    days_remaining = (deadline - date.today()).days
    urgency_score = max(0.0, 100 - max(days_remaining, 0) / 3)
    return DebtClockEntry(
        technology_id=technology_id,
        technology_name=technology_name,
        deadline_type=deadline_type,
        deadline=deadline,
        days_remaining=days_remaining,
        risk_level=risk_from_score(urgency_score),
        migration_complexity=migration_complexity,
        estimated_remediation_effort_days=estimated_remediation_effort_days,
    )


def calculate_variance(req: VarianceAssessmentRequest) -> VarianceAssessment:
    current = set(req.current.platforms)
    target = set(req.target.platforms)

    union = current | target
    delta_ratio = 0.0 if not union else len(current ^ target) / len(union)

    base = round(delta_ratio * 100, 2)
    breakdown = VarianceBreakdown(
        strategic_variance=base,
        cost_variance=round(min(100.0, base * 0.9), 2),
        security_variance=round(min(100.0, base * 1.1), 2),
        talent_variance=round(min(100.0, base * 0.95), 2),
        operational_variance=round(min(100.0, base * 1.05), 2),
        innovation_variance=round(min(100.0, base * 1.15), 2),
    )

    drift = round(
        (
            breakdown.strategic_variance
            + breakdown.cost_variance
            + breakdown.security_variance
            + breakdown.talent_variance
            + breakdown.operational_variance
            + breakdown.innovation_variance
        )
        / 6,
        2,
    )

    return VarianceAssessment(variance_score=base, drift_score=drift, breakdown=breakdown)


def simulate_reality(req: RealitySimulationRequest) -> list[RealityBranch]:
    scale = (req.users / 1000) + (req.servers / 200)
    legacy_load = len(req.technologies)

    return [
        RealityBranch(
            branch_name="Branch A",
            modernization_timing="Modernize Now",
            cost_projection=round(1_200_000 + scale * 50_000, 2),
            staffing_projection_fte=round(14 + scale, 1),
            security_risk_projection=round(max(5.0, 35 - scale), 2),
            technical_debt_projection=round(max(10.0, 40 - scale * 1.2), 2),
            migration_complexity=round(50 + legacy_load * 3.5, 2),
            confidence_score=78.0,
        ),
        RealityBranch(
            branch_name="Branch B",
            modernization_timing="Modernize In 24 Months",
            cost_projection=round(1_000_000 + scale * 48_000, 2),
            staffing_projection_fte=round(12 + scale * 0.9, 1),
            security_risk_projection=round(55 + legacy_load * 2.0, 2),
            technical_debt_projection=round(60 + legacy_load * 2.5, 2),
            migration_complexity=round(65 + legacy_load * 3.5, 2),
            confidence_score=72.0,
        ),
        RealityBranch(
            branch_name="Branch C",
            modernization_timing="Modernize At End Of Support",
            cost_projection=round(800_000 + scale * 45_000, 2),
            staffing_projection_fte=round(10 + scale * 0.85, 1),
            security_risk_projection=round(75 + legacy_load * 2.2, 2),
            technical_debt_projection=round(82 + legacy_load * 2.8, 2),
            migration_complexity=round(78 + legacy_load * 4.1, 2),
            confidence_score=63.0,
        ),
    ]
