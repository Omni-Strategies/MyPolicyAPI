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

@router.get("/")
async def get_all_insurance_requests(db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info("Fetching all insurance requests")
    return requests_repo.get_all_requests(db)   

@router.get("/customers/")
async def get_all_requests_with_customer_details(db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info(f"Fetching all insurance requests with customer details")
    return requests_repo.get_all_requests_with_customer_details(db)


@router.get("/companies/{company_id}/unquoted")
async def get_requests_with_customer_details_excluding_quoted(company_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info(f"Fetching insurance requests for company ID: {company_id} excluding quoted requests")
    return requests_repo.get_requests_with_customer_details_excluding_quoted(db, company_id)

@router.get("/customer/{request_id}")
async def get_insurance_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    logger.info(f"Fetching insurance request {request_id}")
    req = requests_repo.get_request_with_customer_details(db, request_id)

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    return {
        "id": req.id,
        "status": req.status,
        "created_at": req.created_at,
        "type": req.insurance_product.name if req.insurance_product else None,
        "reason": req.reason,
        "request_data": req.request_data,
        "name": (
            f"{req.customers.first_name} {req.customers.last_name}"
            if req.customers else None
        ),
        "dob": req.customers.dob if req.customers else None,
        "email": req.customers.email if req.customers else None,
        "phone": req.customers.phone if req.customers else None,
        "digital_address": req.customers.digital_address if req.customers else None,
    }