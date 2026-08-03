from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, Quotes, InsuranceRequests, InsuranceCompanies 
from schemas import insurance_company_schema, requests_schema
import uuid
import logging
import base64
from schemas.insurance_company_schema import LogoData
logger = logging.getLogger(__name__)

import boto3
import uuid
from config import settings

s3 = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name="us-east-1",
)

def upload_logo(company_id: str, file_bytes: bytes, file_name: str) -> str:
    key = f"logos/{company_id}/{uuid.uuid4()}_{file_name}"
    s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=file_bytes)
    return key

def create_insurance_company(session: Session, company_data: insurance_company_schema.InsuranceCompanyCreate) -> InsuranceCompanies:
    logo_value = company_data.logo
    if isinstance(logo_value, LogoData):
        logo_value = logo_value.base64

    phone_numbers = ["233" + str(num).removeprefix("0") for num in company_data.phone_numbers]

    company = InsuranceCompanies(
        name=company_data.name,
        logo=logo_value,
        emails=company_data.emails,
        phone_numbers=phone_numbers,
        digital_address=company_data.digital_address,
        address_line_1=company_data.address_line_1,
        address_line_2=company_data.address_line_2,
        country=company_data.country,
    )

    try:
        session.add(company)
        session.commit()
        logger.info(f"Insurance company created with ID: {company.id}")
        return company
    except Exception as e:
        logger.error(f"Error occurred while creating insurance company: {e}")
        session.rollback()
        raise




def get_insurance_company_by_id(session: Session, company_id: uuid.UUID) -> Optional[InsuranceCompanies]:
    try:
        company = session.query(InsuranceCompanies).filter(InsuranceCompanies.id == company_id).first()
        if company:
            logger.info(f"Insurance company fetched with ID: {company_id}")
        else:
            logger.warning(f"No insurance company found with ID: {company_id}")
        return company
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance company: {e}")
        session.rollback()
        raise

def get_insurance_company_by_name(session: Session, company_name: str) -> Optional[InsuranceCompanies]:
    try:
        company = session.query(InsuranceCompanies).filter(InsuranceCompanies.name == company_name).first()
        if company:
            logger.info(f"Insurance company fetched with name: {company_name}")
        else:
            logger.warning(f"No insurance company found with name: {company_name}")
        return company
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance company: {e}")
        session.rollback()
        raise

def get_all_companies(session: Session) -> list[InsuranceCompanies]:
    try:
        companies = session.query(InsuranceCompanies).all()
        if companies:
            logger.info("All insurance companies fetched")
        else:
            logger.warning("No insurance companies found")
        return companies
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance companies: {e}")
        raise

def get_insurance_company_by_email(
    session: Session,
    company_email: str
) -> Optional[InsuranceCompanies]:
    try:
        company = (
            session.query(InsuranceCompanies)
            .filter(InsuranceCompanies.emails.any(company_email))
            .first()
        )

        if company:
            logger.info(f"Insurance company fetched with email: {company_email}")
        else:
            logger.warning(f"No insurance company found with email: {company_email}")

        return company

    except Exception as e:
        logger.error(f"Error occurred while fetching insurance company: {e}")
        session.rollback()
        raise
    
def get_insurance_company_by_email_and_phone(
    session: Session,
    company_email: str,
    phone_number: str
) -> Optional[InsuranceCompanies]:
    try:
        company = (
            session.query(InsuranceCompanies)
            .filter(InsuranceCompanies.emails.any(company_email))
            .filter(InsuranceCompanies.phone_numbers.any(phone_number))
            .first()
        )

        if company:
            logger.info(f"Insurance company fetched with email: {company_email} and phone number: {phone_number}")
        else:
            logger.warning(f"No insurance company found with email: {company_email} and phone number: {phone_number}")

        return company

    except Exception as e:
        logger.error(f"Error occurred while fetching insurance company: {e}")
        session.rollback()
        raise

def get_insurance_company_by_phone_number(
    session: Session,
    phone_number: str
) -> Optional[InsuranceCompanies]:
    try:
        company = (
            session.query(InsuranceCompanies)
            .filter(InsuranceCompanies.phone_numbers.any(phone_number))
            .first()
        )

        if company:
            logger.info(f"Insurance company fetched with phone number: {phone_number}")
        else:
            logger.warning(f"No insurance company found with phone number: {phone_number}")

        return company

    except Exception as e:
        logger.error(f"Error occurred while fetching insurance company: {e}")
        session.rollback()
        raise
    
def update_insurance_company(session: Session, company_id: uuid.UUID, updates: insurance_company_schema.InsuranceCompanyUpdate) -> Optional[InsuranceCompanies]:
    logo = updates.logo

    if isinstance(logo, LogoData):
        file_bytes = base64.b64decode(logo.base64)
        logo_key = upload_logo(company_id, file_bytes, logo.fileName)
        updates.logo = logo_key
    elif isinstance(logo, dict) and "base64" in logo and "fileName" in logo:
        file_bytes = base64.b64decode(logo["base64"])
        logo_key = upload_logo(company_id, file_bytes, logo["fileName"])
        updates.logo = logo_key

    try:
        company = session.query(InsuranceCompanies).filter(InsuranceCompanies.id == company_id).first()
        if not company:
            logger.warning(f"No insurance company found with ID: {company_id}")
            return None

        for key, value in updates.dict(exclude_unset=True).items():
            setattr(company, key, value)

        session.commit()
        logger.info(f"Insurance company updated with ID: {company_id}")

        return company
    except Exception as e:
        logger.error(f"Error occurred while updating insurance company: {e}")
        session.rollback()
        raise

def delete_insurance_company(session: Session, company_id: uuid.UUID) -> bool:
    try:
        company = session.query(InsuranceCompanies).filter(InsuranceCompanies.id == company_id).first()
        if not company:
            logger.warning(f"No insurance company found with ID: {company_id}")
            return False

        session.delete(company)
        session.commit()
        logger.info(f"Insurance company deleted with ID: {company_id}")

        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting insurance company: {e}")
        session.rollback()
        raise