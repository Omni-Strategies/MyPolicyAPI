from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Base, FormRequests, Admins
from schemas import admin_schema, requests_schema, admin_schema
import uuid
import logging
from security.password import *
import json

logger = logging.getLogger(__name__)

def create_admin(
    session: Session,
    admin: admin_schema.adminCreateUserInterface
) -> Admins:
    try:
        # Convert Pydantic → dict
        data = admin.model_dump()

        # Hash password
        data["password"] = hash_password(data["password"])

        # FIX IMAGE (dict → JSON string for VARCHAR column)
        if data.get("image") is not None:
            image_value = data["image"]

            # If it's a Pydantic model
            if hasattr(image_value, "model_dump"):
                image_value = image_value.model_dump()

            # Convert dict → string
            data["image"] = json.dumps(image_value)

        # Ensure roles is safe (UUID array handled by SQLAlchemy)
        if data.get("roles") is None:
            data["roles"] = []

        # Create DB object
        db_admin = Admins(**data)

        session.add(db_admin)
        session.commit()
        session.refresh(db_admin)

        logger.info(f"Admin created with ID: {db_admin.id}")

        return db_admin

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while creating admin: {e}")
        raise

   
def get_admin(session: Session, admin_id: uuid.UUID) -> Optional[Admins]:
    try:
        admin = session.query(Admins).filter(Admins.id == admin_id).first()
        if admin:
            logger.info(f"admin fetched with ID: {admin_id}")
        else:
            logger.warning(f"No admin found with ID: {admin_id}")
        return admin
    except Exception as e:
        logger.error(f"Error occurred while fetching admin: {e}")
        session.rollback()
        raise

def get_admin_by_email(session: Session, admin_email: str):
    try:
        admin = session.query(Admins).filter(Admins.email == admin_email).first()
        if admin:
            logger.info(f"admin fetched with email: {admin_email}")
        else:
            logger.warning(f"No csutomer found with email {admin_email}")
        return admin
    except Exception as e:
        logger.error(f"Error occured while fetching admin: {e}")
        session.rollback()
        raise




def update_admin(
    session: Session,
    admin: admin_schema.adminUpdateUserInterface,
    admin_id: uuid.UUID
) -> Optional[Admins]:

    try:
        db_admin = session.query(Admins).filter(Admins.id == admin_id).first()

        if not db_admin:
            return None

        data = admin.model_dump(exclude_unset=True)

        for key, value in data.items():

            if hasattr(db_admin, key):

                # 🔥 SPECIAL FIX FOR IMAGE FIELD
                if key == "image" and value is not None:
                    if hasattr(value, "model_dump"):
                        value = value.model_dump()

                    value = json.dumps(value)  # convert dict → string

                setattr(db_admin, key, value)

        session.commit()
        session.refresh(db_admin)

        logger.info(f"admin updated with ID: {admin_id}")

        return db_admin

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while updating admin: {e}")
        raise
    

def delete_admin(session: Session, admin_id: uuid.UUID) -> bool:
    try:
        db_admin = session.query(Admins).filter(Admins.id == admin_id).first()
        if not db_admin:
            return False
        session.delete(db_admin)
        session.commit()
        logger.info(f"admin deleted with ID: {admin_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting admin: {e}")
        session.rollback()
        raise
