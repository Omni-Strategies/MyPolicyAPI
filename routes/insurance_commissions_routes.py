from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import insurance_commissions_repo
from schemas import insurance_commissions_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *

router = APIRouter(tags=["insurance_commissions"])

logger = logging.getLogger(__name__)

@router.post("/create")
async def create_insurance_commissions(insurance_commissions: insurance_commissions_schema.insuranceCommissionCreateInterface, db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info(f"Creating insurance commission with data: {insurance_commissions.dict()}")
    return insurance_commissions_repo.create_insurance_commissions(db, insurance_commissions) 

@router.get("/get")
async def get_insurane_commissions(insurance_commissions_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Fetching form request with ID: {insurance_commissions_id}")
    return insurance_commissions_repo.get_insurance_commission(db, insurance_commissions_id)

@router.get("/get/{company_id}")
async def get_insurance_commissions_by_company_id(company_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info(f"Fetching insurance commissions with company ID: {company_id}")
    return insurance_commissions_repo.get_insurance_commissions_by_company_id(db, company_id)

@router.patch("/update/{commissions_id}")
async def update_insurance_commissions(commissions_id: uuid.UUID, insurance_commissions_update: insurance_commissions_schema.InsuranceCommissionUpdateInterface, db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info(f"Updating insurance commissions with commissions ID: {commissions_id}")
    return insurance_commissions_repo.update_insurance_commission(db, insurance_commissions_update, commissions_id)

@router.delete("/delete/{commissions_id}")
async def delete_insurance_commissions(commissions_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(company_admin_required)):
    logger.info(f"deleting insurance commissions with ID {commissions_id}")
    return insurance_commissions_repo.delete_insurance_commission(db, commissions_id)