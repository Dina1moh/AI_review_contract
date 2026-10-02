# routes/risk_route.py
import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException

CURRENT_DIR = Path(__file__).resolve().parent
APP_DIR = CURRENT_DIR.parent
RISK_ENGINE_DIR = APP_DIR / "Core" / "Risk-assisment"
sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(RISK_ENGINE_DIR))

from inferance import execute_risk_inference
from schemas.risk_schema import RiskAssessmentResponse

router = APIRouter(prefix="/api/v1/risk", tags=["Risk Assessment Node"])

@router.post("/evaluate", response_model=RiskAssessmentResponse)
def evaluate_clause_node(clause_text: str, category_name: str):
    """
    Live standalone evaluation node to benchmark Stage 3 pipeline metrics.
    """
    try:
        result = execute_risk_inference(clause_text, category_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal audit failure: {str(e)}")
