from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import requests_repo
from schemas import insurance_company_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *
from repositories import insurance_company_repo
import boto3
from fastapi.responses import StreamingResponse
from config import settings
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/insurance-companies", tags=["insurance_company"])
logger = logging.getLogger(__name__)
s3 = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,   # internal: http://minio:9000
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name="us-east-1",
)
@router.post("/")
async def create_insurance_company(insurance_company: insurance_company_schema.InsuranceCompanyCreate,
                                     db: Session = Depends(get_db),
                                     ):
    logger.info(f"Creating insurance company with data: {insurance_company.dict()}")
    return insurance_company_repo.create_insurance_company(db, insurance_company)

@router.get("/all")
async def get_all_insirance_companies(          db: Session = Depends(get_db),
                                                current_user=Depends(admin_required)):
    logger.info(f"Fetching insurance companies")
    return insurance_company_repo.get_all_companies(db)

@router.get("/{company_id}")
async def get_insurance_company(company_id: uuid.UUID,
                                 db: Session = Depends(get_db),
                                 current_user=Depends(company_admin_required)):
    logger.info(f"Fetching insurance company with ID: {company_id}")
    return insurance_company_repo.get_insurance_company_by_id(db, company_id)

@router.get("/emails/{company_email}")
async def get_insurance_company(company_email: str,
                                 db: Session = Depends(get_db),
                                 current_user=Depends(admin_required)):
    logger.info(f"Fetching insurance company with email: {company_email}")
    return insurance_company_repo.get_insurance_company_by_email(db, company_email)

@router.get("/phone/{phone_number}")
async def get_insurance_company_by_phone_number(phone_number: str,
                                                db: Session = Depends(get_db),
                                                current_user=Depends(admin_required)):
    logger.info(f"Fetching insurance company with phone number: {phone_number}")
    return insurance_company_repo.get_insurance_company_by_phone_number(db, phone_number)


@router.patch("/updates/{company_id}")
async def update_insurance_company(company_id: uuid.UUID,
                                    updates: insurance_company_schema.InsuranceCompanyUpdate,
                                     db: Session = Depends(get_db),
                                     current_user=Depends(company_admin_required)):
    logger.info(f"Updating insurance company with ID: {company_id}")
    return insurance_company_repo.update_insurance_company(db, company_id, updates)

@router.delete("/delete/{company_id}")
async def delete_insurance_company(company_id: uuid.UUID,
                                     db: Session = Depends(get_db),
                                     current_user=Depends(admin_required)):
    logger.info(f"Deleting insurance company with ID: {company_id}")
    return insurance_company_repo.delete_insurance_company(db, company_id)

@router.get("/{company_id}/logo")
async def get_company_logo(company_id: uuid.UUID, db: Session = Depends(get_db)):
    company = db.query(InsuranceCompanies).filter(InsuranceCompanies.id == company_id).first()
    if not company or not company.logo:
        raise HTTPException(status_code=404, detail="Logo not found")

    s3_object = s3.get_object(Bucket=settings.S3_BUCKET, Key=company.logo)
    return StreamingResponse(s3_object["Body"], media_type="image/jpeg")