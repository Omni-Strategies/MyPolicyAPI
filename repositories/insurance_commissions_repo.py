from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, Quotes, InsuranceRequests, InsuranceCompanies, InsuranceCommissions 
from schemas import insurance_commissions_schema, insurance_company_schema, requests_schema
import uuid
import logging

logger = logging.getLogger(__name__)

def create_insurance_commissions(session: Session, insurance_commission_request: insurance_commissions_schema.insuranceCommissionCreateInterface) -> InsuranceCommissions:
    db_commission_request = InsuranceCommissions(**insurance_commission_request.dict())
    try:
            session.add(db_commission_request)
            session.commit()
            session.refresh(db_commission_request)
            logger.info(f"Form request created with ID: {db_commission_request.id}")
            return db_commission_request
    except Exception as e:
            logger.error(f"Error occurred while creating form request: {e}")
            session.rollback()
            raise

def get_insurance_commission(session: Session, commissions_id: uuid.UUID) -> InsuranceCommissions:
    try:
            commissions = session.query(InsuranceCommissions).filter(InsuranceCommissions.id == commissions_id).first()
            if commissions:
                logger.info(f"Form request fetched with ID: {commissions_id}")
            else:
                logger.warning(f"No form request found with ID: {commissions_id}")
            return commissions
    except Exception as e:
            logger.error(f"Error occurred while fetching form request: {e}")
            raise


def get_insurance_commissions_by_company_id(session: Session, company_id: uuid.UUID) -> InsuranceCommissions:
    try:
            commissions = session.query(InsuranceCommissions).filter(InsuranceCommissions.insurance_company_id == company_id).all()
            if commissions:
                logger.info(f"Form request fetched with ID: {company_id}")
            else:
                logger.warning(f"No form request found with ID: {company_id}")
            return commissions
    except Exception as e:
            logger.error(f"Error occurred while fetching form request: {e}")
            raise

def update_insurance_commission(session: Session, insurance_commission_request: insurance_commissions_schema.InsuranceCommissionUpdateInterface, insurance_commissions_request_id: uuid.UUID) -> Optional[InsuranceCommissions]:
    try:
        db_insurance_commission_request = session.query(InsuranceCommissions).filter(InsuranceCommissions.id == insurance_commissions_request_id).first()
        if not db_insurance_commission_request:
            return None
        for key, value in insurance_commission_request.dict(exclude_unset=True).items():
            if hasattr(db_insurance_commission_request, key):
                setattr(db_insurance_commission_request, key, value)
        session.add(db_insurance_commission_request)
        session.commit()
        session.refresh(db_insurance_commission_request)
        return db_insurance_commission_request
    except Exception as e:
        logger.error(f"Error occurred while updating form request: {e}")
        session.rollback()
        raise

def delete_insurance_commission(session: Session, insurance_commissions_id: uuid.UUID) -> bool:
    try:
        db_insurance_commission_request = session.query(InsuranceCommissions).filter(InsuranceCommissions.id == insurance_commissions_id).first()
        if not db_insurance_commission_request:
            return False
        session.delete(db_insurance_commission_request)
        session.commit()
        logger.info(f"Form request deleted with ID: {insurance_commissions_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting form request: {e}")
        session.rollback()
        raise