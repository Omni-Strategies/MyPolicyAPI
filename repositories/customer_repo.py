from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, Customers, FormRequests  
from schemas import customer_schema, requests_schema
import uuid
import logging
from security.password import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_customer(
    session: Session,
    customer: customer_schema.CustomerRegisterInterface
) -> Customers:

    try:
        customer.password = hash_password(customer.password)

        db_customer = Customers(**customer.dict())

        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)

        logger.info(
            f"Customer created with ID: {db_customer.id}"
        )

        return db_customer

    except Exception as e:
        logger.error(
            f"Error occurred while creating customer: {e}"
        )
        session.rollback()
        raise
    
def get_customer(session: Session, customer_id: uuid.UUID) -> Optional[Customers]:
    try:
        customer = session.query(Customers).filter(Customers.id == customer_id).first()
        if customer:
            logger.info(f"Customer fetched with ID: {customer_id}")
        else:
            logger.warning(f"No customer found with ID: {customer_id}")
        return customer
    except Exception as e:
        logger.error(f"Error occurred while fetching customer: {e}")
        session.rollback()
        raise

def get_customer_by_email(session: Session, customer_email: str):
    try:
        customer = session.query(Customers).filter(Customers.email == customer_email).first()
        if customer:
            logger.info(f"Customer fetched with email: {customer_email}")
        else:
            logger.warning(f"No csutomer found with email {customer_email}")
        return customer
    except Exception as e:
        logger.error(f"Error occured while fetching customer: {e}")
        session.rollback()
        raise




def update_customer(session: Session, customer: customer_schema.customerUpdateUserInterface, customer_id: uuid.UUID) -> Optional[Customers]:
    try:
        db_customer = session.query(Customers).filter(Customers.id == customer_id).first()
        if not db_customer:
            return None
        for key, value in customer.dict().items():
            if hasattr(db_customer, key):
                setattr(db_customer, key, value)
        session.add(db_customer)
        session.commit()
        logger.info(f"Customer updated with ID: {customer_id}")
        return db_customer
    except Exception as e:
        logger.error(f"Error occurred while updating customer: {e}")
        session.rollback()
        raise
    

def delete_customer(session: Session, customer_id: uuid.UUID) -> bool:
    try:
        db_customer = session.query(Customers).filter(Customers.id == customer_id).first()
        if not db_customer:
            return False
        session.delete(db_customer)
        session.commit()
        logger.info(f"Customer deleted with ID: {customer_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting customer: {e}")
        session.rollback()
        raise
