from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field, model_validator


class RiskLevel(str, Enum):
    green = "green"
    amber = "amber"
    red = "red"


class Technology(BaseModel):
    id: str
    name: str
    vendor: str
    category: str


class LifecycleEvent(BaseModel):
    technology_id: str
    event_type: str
    event_date: date


class MortalityInput(BaseModel):
    technology_id: str
    adoption_score: float = Field(ge=0, le=100)
    community_momentum_score: float = Field(ge=0, le=100)
    vendor_investment_score: float = Field(ge=0, le=100)
    talent_availability_score: float = Field(ge=0, le=100)
    migration_urgency_score: float = Field(ge=0, le=100)


class MortalityWeights(BaseModel):
    adoption_weight: float = Field(default=0.2, ge=0.0, le=1.0, allow_inf_nan=False)
    community_weight: float = Field(default=0.2, ge=0.0, le=1.0, allow_inf_nan=False)
    vendor_weight: float = Field(default=0.2, ge=0.0, le=1.0, allow_inf_nan=False)
    talent_weight: float = Field(default=0.2, ge=0.0, le=1.0, allow_inf_nan=False)
    migration_weight: float = Field(default=0.2, ge=0.0, le=1.0, allow_inf_nan=False)

    @model_validator(mode="after")
    def _validate_normalized_total(self) -> "MortalityWeights":
        total = (
            self.adoption_weight
            + self.community_weight
            + self.vendor_weight
            + self.talent_weight
            + self.migration_weight
        )
        if abs(total - 1.0) > 1e-9:
            raise ValueError("Mortality weights must sum to 1.0")
        return self


class TechnologyMortality(BaseModel):
    technology_id: str
    mortality_score: float
    risk_level: RiskLevel


class DebtClockEntry(BaseModel):
    technology_id: str
    technology_name: str
    deadline_type: str
    deadline: date
    days_remaining: int
    risk_level: RiskLevel
    migration_complexity: str
    estimated_remediation_effort_days: int


class VarianceState(BaseModel):
    platforms: List[str] = Field(default_factory=list)


class VarianceAssessmentRequest(BaseModel):
    current: VarianceState
    target: VarianceState


class VarianceBreakdown(BaseModel):
    strategic_variance: float
    cost_variance: float
    security_variance: float
    talent_variance: float
    operational_variance: float
    innovation_variance: float


class VarianceAssessment(BaseModel):
    variance_score: float
    drift_score: float
    breakdown: VarianceBreakdown


class RealityBranch(BaseModel):
    branch_name: str
    modernization_timing: str
    cost_projection: float
    staffing_projection_fte: float
    security_risk_projection: float
    technical_debt_projection: float
    migration_complexity: float
    confidence_score: float


class RealitySimulationRequest(BaseModel):
    users: int = Field(gt=0, le=1_000_000)
    servers: int = Field(gt=0, le=100_000)
    technologies: List[str] = Field(default_factory=list, max_length=50)


class RealitySimulationResponse(BaseModel):
    branches: List[RealityBranch]


class DashboardSummary(BaseModel):
    technology_health_score: float
    debt_exposure_count: int
    upcoming_deadlines: int
    mortality_exposure_count: int
    budget_impact_forecast: float
    top_risks: List[str]


class OrganizationProfile(BaseModel):
    id: str
    name: str
    strategic_destination: str


class TechnologySignal(BaseModel):
    technology_id: str
    source: str
    signal_type: str
    sentiment: str


class Forecast(BaseModel):
    technology_id: str
    horizon_months: int
    values: Dict[str, float]


class CommunityInsight(BaseModel):
    technology: str = Field(..., max_length=100)
    expected_outcome: str = Field(..., max_length=500)
    actual_outcome: str = Field(..., max_length=500)
    would_repeat: bool
    migration_duration_months: int = Field(..., ge=0, le=600)
    lessons_learned: str = Field(..., max_length=1000)
