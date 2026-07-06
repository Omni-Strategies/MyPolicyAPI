from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import form_requests_repo
from schemas import form_requests_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *

router = APIRouter(tags=["form_requests"])

logger = logging.getLogger(__name__)

@router.post("/form_requests")
async def create_form_request(form_request: form_requests_schema.FormRequestCreateInterface, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Creating form request with data: {form_request.dict()}")
    return form_requests_repo.create_form_request(db, form_request) 

@router.get("/form_requests")
async def get_all_form_requests(db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info("Fetching all form requests")
    return form_requests_repo.get_all_form_requests(db)

@router.get("/form_requests/{form_request_id}")
async def get_form_request(form_request_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Fetching form request with ID: {form_request_id}")
    return form_requests_repo.get_form_request(db, form_request_id)

@router.put("/form_requests/{form_request_id}")
async def update_form_request(form_request_id: uuid.UUID, updates: form_requests_schema.FormRequestUpdateInterface, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Updating form request with ID: {form_request_id}")
    return form_requests_repo.update_form_request(db, updates, form_request_id)

@router.delete("/form_requests/{form_request_id}")
async def delete_form_request(form_request_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Deleting form request with ID: {form_request_id}")
    return form_requests_repo.delete_form_request(db, form_request_id)