from typing import Literal

from pydantic import BaseModel, Field


class RiskAssessmentResponse(BaseModel):
    assessment_status: Literal["violation", "no_violation", "insufficient_evidence", "not_applicable"] = Field(
        default="insufficient_evidence",
        description="Whether this clause-level review found a supported risk or had enough evidence to assess it",
    )
    has_violation: bool = Field(default=False, description="Flag identifying if any textbook guidelines were broken")
    failed_checklist_question: str = Field(default="", description="The EduRisk checklist ID and question that failed, if any")
    not_assessed_questions: list[str] = Field(
        default_factory=list,
        description="Checklist IDs that require the full contract, institutional policy, or human input",
    )
    clause_contradiction: str = Field(default="", description="Direct quotation of the risky text from the target clause")
    correct_rule_from_book: str = Field(default="", description="The correct legal standard extracted from the textbook")
    risk_tier: str = Field(default="Unknown", description="Risk severity: None, Low, Medium, High, or Unknown")
    recommendation: str = Field(default="", description="Actionable drafting advice for the attorney to fix the script")