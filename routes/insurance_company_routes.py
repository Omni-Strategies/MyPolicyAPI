from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import requests_repo
from schemas import insurance_company_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *
from repositories import insurance_company_repo

router = APIRouter(prefix="/insurance-companies", tags=["insurance_company"])
logger = logging.getLogger(__name__)

@router.post("/")
async def create_insurance_company(insurance_company: insurance_company_schema.InsuranceCompanyCreate,
                                     db: Session = Depends(get_db),
                                     current_user=Depends(admin_required)):
    logger.info(f"Creating insurance company with data: {insurance_company.dict()}")
    return insurance_company_repo.create_insurance_company(db, insurance_company)


@router.get("/{company_id}")
async def get_insurance_company(company_id: uuid.UUID,
                                 db: Session = Depends(get_db),
                                 current_user=Depends(admin_required)):
    logger.info(f"Fetching insurance company with ID: {company_id}")
    return insurance_company_repo.get_insurance_company(db, company_id)

@router.get("/emails/{company_email}")
async def get_insurance_company(company_email: str,
                                 db: Session = Depends(get_db),
                                 current_user=Depends(admin_required)):
    logger.info(f"Fetching insurance company with email: {company_email}")
    return insurance_company_repo.get_insurance_company_by_email(db, company_email)

@router.put("/updates/{company_id}")
async def update_insurance_company(company_id: uuid.UUID,
                                    updates: insurance_company_schema.InsuranceCompanyUpdate,
                                     db: Session = Depends(get_db),
                                     current_user=Depends(admin_required)):
    logger.info(f"Updating insurance company with ID: {company_id}")
    return insurance_company_repo.update_insurance_company(db, company_id, updates)

@router.delete("/delete/{company_id}")
async def delete_insurance_company(company_id: uuid.UUID,
                                     db: Session = Depends(get_db),
                                     current_user=Depends(admin_required)):
    logger.info(f"Deleting insurance company with ID: {company_id}")
    return insurance_company_repo.delete_insurance_company(db, company_id)