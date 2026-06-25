from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from repositories import admin_repo
from schemas import admin_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admins", tags=["admins"])

@router.post("/")
async def create_admin(admin: admin_schema.adminCreateUserInterface, db: Session = Depends(get_db)):
    logger.info(f"Creating admin with data: {admin.dict()}")
    return admin_repo.create_admin(db, admin)

@router.get("/{admin_id}")
async def get_admin(admin_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    logger.info(f"Fetching admin with ID: {admin_id}")
    return admin_repo.get_admin(db, admin_id)

@router.put("/updates/{admin_id}")
async def update_admin(admin_id: uuid.UUID, updates: admin_schema.adminUpdateUserInterface, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    logger.info(f"Updating admin with ID: {admin_id}")
    return admin_repo.update_admin(db, updates, admin_id)

@router.delete("/delete/{admin_id}")
async def delete_admin(admin_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    logger.info(f"Deleting admin with ID: {admin_id}")
    return admin_repo.delete_admin(db, admin_id)