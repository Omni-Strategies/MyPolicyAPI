from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import requests_repo
from schemas import requests_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/")
async def create_insurance_request(request: requests_schema.InsuranceRequestCreateInterface, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Creating insurance request with data: {request.dict()}")
    return requests_repo.create_request(db, request)


@router.get("/{request_id}")
async def get_insurance_request(request_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Fetching insurance request with ID: {request_id}")
    return requests_repo.get_request(db, request_id)

@router.put("/updates/{request_id}")
async def update_insurance_request(request_id: uuid.UUID, updates: requests_schema.InsuranceRequestUpdateInterface, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Updating insurance request with ID: {request_id}")
    return requests_repo.update_request(db, updates, request_id)

@router.delete("/delete/{request_id}")
async def delete_insurance_request(request_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Deleting insurance request with ID: {request_id}")
    return requests_repo.delete_request(db, request_id)
