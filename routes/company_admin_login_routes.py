from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import logging
from security.auth import create_access_token
from fastapi import APIRouter, Depends
from database import get_db
from models.models import *
from schemas import insurance_company_schema
from sqlalchemy.orm import Session
import logging
from security.dependencies import *
from repositories.insurance_company_repo import *

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/company-login", tags=["company_admin_login"])

class CompanyAdminLoginRequest(BaseModel):
    email: str


@router.post("/company-admin-login")
def company_admin_login(
    request: CompanyAdminLoginRequest,
    db: Session = Depends(get_db)
):
    company_admin = get_insurance_company_by_email(db, request.email)

    if not company_admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": create_access_token({
            "sub": str(company_admin.id),
            "account_type": "company_admin"
        }),
        "token_type": "bearer"
    }