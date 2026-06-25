from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, Customers, FormRequests  
from schemas import form_requests_schema, customer_schema
import uuid
import logging

logger = logging.getLogger(__name__)

def create_form_request(session: Session, form_request: form_requests_schema.FormRequestCreateInterface) -> FormRequests:
    db_form_request = FormRequests(**form_request.dict())
    try:
        session.add(db_form_request)
        session.commit()
        session.refresh(db_form_request)
        logger.info(f"Form request created with ID: {db_form_request.id}")
        return db_form_request
    except Exception as e:
        logger.error(f"Error occurred while creating form request: {e}")
        session.rollback()
        raise

def get_all_form_requests(session: Session) -> List[FormRequests]:
    try:
        form_requests = session.query(FormRequests).all()
        logger.info(f"Fetched {len(form_requests)} form requests")
        return form_requests
    except Exception as e:
        logger.error(f"Error occurred while fetching form requests: {e}")
        raise


def get_form_request(session: Session, form_request_id: uuid.UUID) -> Optional[FormRequests]:
    try:
        form_request = session.query(FormRequests).filter(FormRequests.id == form_request_id).first()
        if form_request:
            logger.info(f"Form request fetched with ID: {form_request_id}")
        else:
            logger.warning(f"No form request found with ID: {form_request_id}")
        return form_request
    except Exception as e:
        logger.error(f"Error occurred while fetching form request: {e}")
        raise

def update_form_request(session: Session, form_request: form_requests_schema.FormRequestUpdateInterface, form_request_id: uuid.UUID) -> Optional[FormRequests]:
    try:
        db_form_request = session.query(FormRequests).filter(FormRequests.id == form_request_id).first()
        if not db_form_request:
            return None
        for key, value in form_request.dict().items():
            if hasattr(db_form_request, key):
                setattr(db_form_request, key, value)
        session.add(db_form_request)
        session.commit()
        session.refresh(db_form_request)
        return db_form_request
    except Exception as e:
        logger.error(f"Error occurred while updating form request: {e}")
        session.rollback()
        raise
    

def delete_form_request(session: Session, form_request_id: uuid.UUID) -> bool:
    try:
        db_form_request = session.query(FormRequests).filter(FormRequests.id == form_request_id).first()
        if not db_form_request:
            return False
        session.delete(db_form_request)
        session.commit()
        logger.info(f"Form request deleted with ID: {form_request_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting form request: {e}")
        session.rollback()
        raise