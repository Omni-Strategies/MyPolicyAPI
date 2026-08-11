from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.models import InsuranceCompanies
from schemas import insurance_company_schema
from s3_client import upload_logo
from otp_delivery import normalize_phone, phone_lookup_variants
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

class InsuranceCompanyConflictError(Exception):
    """Raised when email or phone already belongs to another company."""


def _email_or_phone_taken(
    session: Session,
    emails: list[str],
    phone_numbers: list[str],
) -> Optional[str]:
    for email in emails or []:
        if get_insurance_company_by_email(session, email):
            return f"Email already registered: {email}"
    for phone in phone_numbers or []:
        if get_insurance_company_by_phone_number(session, phone):
            return f"Phone number already registered: {phone}"
    return None


def create_insurance_company(session: Session, company_data: insurance_company_schema.InsuranceCompanyCreate) -> InsuranceCompanies:
    try:
        data = company_data.dict()
        data["phone_numbers"] = [
            normalize_phone(p) for p in (data.get("phone_numbers") or []) if normalize_phone(p)

        conflict = _email_or_phone_taken(
            session,
            data.get("emails") or [],
            data.get("phone_numbers") or [],
        )
        if conflict:
            raise InsuranceCompanyConflictError(conflict)

        data["logo"] = upload_logo(data.get("logo"))

        db_insurance_company = InsuranceCompanies(**data)
        session.add(db_insurance_company)
        session.commit()
        session.refresh(db_insurance_company)
        logger.info(f"Insurance company created with ID: {db_insurance_company.id}")
        return db_insurance_company
    except InsuranceCompanyConflictError:
        session.rollback()
        raise
    except Exception as e:
        logger.error(f"Error occurred while creating insurance company: {e}")
        session.rollback()
        raise


def get_insurance_company(session: Session, company_id: uuid.UUID) -> Optional[InsuranceCompanies]:
    return get_insurance_company_by_id(session, company_id)


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
        variants = phone_lookup_variants(phone_number)
        if not variants:
            return None

        company = (
            session.query(InsuranceCompanies)
            .filter(or_(*[InsuranceCompanies.phone_numbers.any(v) for v in variants]))
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

        data = updates.dict(exclude_unset=True)
        if "logo" in data:
            data["logo"] = upload_logo(data.get("logo"))

        for key, value in data.items():
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