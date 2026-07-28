from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, Quotes, InsuranceRequests, InsuranceCompanies 
from schemas import insurance_company_schema, requests_schema
import uuid
import logging

logger = logging.getLogger(__name__)


def create_insurance_company(session: Session, company_data: insurance_company_schema.InsuranceCompanyCreate) -> InsuranceCompanies:
    try:
        company = InsuranceCompanies(
            name=company_data.name,
            logo=company_data.logo
        )

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