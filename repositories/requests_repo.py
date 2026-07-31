from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models.models import Base, FormRequests, InsuranceRequests, Quotes  
from schemas import requests_schema
import uuid
import logging

logger = logging.getLogger(__name__)

def create_request(session: Session, request: requests_schema.InsuranceRequestCreateInterface) -> InsuranceRequests:
    db_request = InsuranceRequests(**request.dict())
    try:
        session.add(db_request)
        session.commit()
        session.refresh(db_request)
        logger.info(f"Insurance request created with ID: {db_request.id}")
        return db_request
    except Exception as e:
        logger.error(f"Error occurred while creating insurance request: {e}")
        session.rollback()
        raise
    

def get_all_requests(session: Session) -> List[InsuranceRequests]:
    try:
        requests = session.query(InsuranceRequests).all()
        logger.info(f"Fetched {len(requests)} insurance requests")
        return requests
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance requests: {e}")
        session.rollback()
        raise

def get_requests_with_customer_details_excluding_quoted(session: Session, company_id: uuid.UUID) -> List[InsuranceRequests]:
    quoted_ids = (
        session.query(Quotes.insurance_request_id)
        .filter(Quotes.insurance_company_id == company_id)
        .subquery()
    )

    requests = (
        session.query(InsuranceRequests)
        .options(
            joinedload(InsuranceRequests.customers),
            joinedload(InsuranceRequests.insurance_product),
        )
        .filter(InsuranceRequests.id.notin_(quoted_ids))
        .filter(InsuranceRequests.status == "pending")
        .all()
    )
    return requests
def get_request(session: Session, request_id: uuid.UUID) -> Optional[InsuranceRequests]:
    try:
        request = session.query(InsuranceRequests).filter(InsuranceRequests.id == request_id).first()
        if request:
            logger.info(f"Insurance request fetched with ID: {request_id}")
        else:
            logger.warning(f"No insurance request found with ID: {request_id}")
        return request
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance request: {e}")
        session.rollback()
        raise


def get_requests_by_customer(session: Session, customer_id: uuid.UUID) -> List[InsuranceRequests]:
    try:
        requests = (
            session.query(InsuranceRequests)
            .options(joinedload(InsuranceRequests.insurance_product))
            .filter(InsuranceRequests.requested_by == customer_id)
            .filter(InsuranceRequests.deleted.is_(False))
            .order_by(InsuranceRequests.created_at.desc())
            .all()
        )
        logger.info(f"Fetched {len(requests)} insurance requests for customer {customer_id}")
        return requests
    except Exception as e:
        logger.error(f"Error occurred while fetching requests for customer {customer_id}: {e}")
        session.rollback()
        raise

def get_request_with_customer_details(session: Session, request_id: uuid.UUID) -> Optional[InsuranceRequests]:
    try:
        request = (
            session.query(InsuranceRequests)
            .options(
                joinedload(InsuranceRequests.customers),
                joinedload(InsuranceRequests.insurance_product),
            )
            .filter(InsuranceRequests.id == request_id)
            .first()
        )
        if request:
            logger.info(f"Insurance request fetched with ID: {request_id}")
        else:
            logger.warning(f"No insurance request found with ID: {request_id}")
        return request
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance request: {e}")
        session.rollback()
        raise

def update_request(session: Session, request: requests_schema.InsuranceRequestUpdateInterface, request_id: uuid.UUID) -> Optional[InsuranceRequests]:
    try:
        db_request = session.query(InsuranceRequests).filter(InsuranceRequests.id == request_id).first()
        if not db_request:
            return None
        for key, value in request.dict().items():
            if hasattr(db_request, key):
                setattr(db_request, key, value)
        session.add(db_request)
        session.commit()
        session.refresh(db_request)
        return db_request
    except Exception as e:
        logger.error(f"Error occurred while updating insurance request: {e}")
        session.rollback()
        raise


def delete_request(session: Session, request_id: uuid.UUID) -> bool:
    try:
        db_request = session.query(InsuranceRequests).filter(InsuranceRequests.id == request_id).first()
        if not db_request:
            return False
        session.delete(db_request)
        session.commit()
        logger.info(f"Insurance request deleted with ID: {request_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting insurance request: {e}")
        session.rollback()
        raise                                
   
def get_all_requests_with_customer_details(session: Session) -> List[InsuranceRequests]:
    try:
        requests = (
            session.query(InsuranceRequests)
            .options(
                joinedload(InsuranceRequests.customers),
                joinedload(InsuranceRequests.insurance_product),
            )
            .all()
        )
        logger.info(f"Fetched {len(requests)} insurance requests")
        return requests
    except Exception as e:
        logger.error(f"Error occurred while fetching insurance requests: {e}")
        session.rollback()
        raise