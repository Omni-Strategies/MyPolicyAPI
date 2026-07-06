from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import customer_repo
from schemas import customer_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *

        
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/")
async def create_customer(customer: customer_schema.CustomerRegisterInterface, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Creating customer with data: {customer.dict()}")
    return customer_repo.create_customer(db, customer)

@router.get("/{customer_id}")
async def get_customer(customer_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Fetching customer with ID: {customer_id}")
    return customer_repo.get_customer(db, customer_id)

@router.put("/updates/{customer_id}")
async def update_customer(customer_id: uuid.UUID, updates: customer_schema.customerUpdateUserInterface, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Updating customer with ID: {customer_id}")
    return customer_repo.update_customer(db, updates, customer_id)

@router.delete("/delete/{customer_id}")
async def delete_customer(customer_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(customer_required)):
    logger.info(f"Deleting customer with ID: {customer_id}")
    return customer_repo.delete_customer(db, customer_id)