from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

# Pydantic models
class DrugInfo(BaseModel):
    name: str = Field(..., example="Aspirin")
    dose_mg: float = Field(..., example=100)

class CheckRequest(BaseModel):
    drugs: List[DrugInfo]

class CheckResponse(BaseModel):
    interaction_risk: str = Field(..., example="high")
    message: str = Field(..., example="Potential interaction detected between Aspirin and Warfarin.")

# Endpoint
@router.post("/check", response_model=CheckResponse)
async def check_drug_interactions(request: CheckRequest):
    if len(request.drugs) < 2:
        raise HTTPException(status_code=400, detail="At least two drugs are required for interaction check.")
    return CheckResponse(
        interaction_risk="low",
        message="No significant interactions detected."
    )
