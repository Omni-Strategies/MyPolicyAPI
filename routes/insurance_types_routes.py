# routers/insurance_types.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from schemas.insurance_types_schemas import InsuranceTypeOut
from models.models import InsuranceProducts

router = APIRouter(prefix="/insurance-types", tags=["insurance-types"])

@router.get("", response_model=list[InsuranceTypeOut])
def list_insurance_types(db: Session = Depends(get_db)):
    result = db.execute(select(InsuranceProducts))
    return result.scalars().all()