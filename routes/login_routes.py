from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from repositories.admin_repo import get_admin_by_email
from repositories.insurance_company_repo import get_insurance_company_by_email, get_insurance_company_by_phone_number
from security.password import verify_password
from security.auth import create_access_token
from repositories.customer_repo import get_customer_by_email
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    admin = get_admin_by_email(db, email)

    if admin and verify_password(password, admin.password):
        return {
            "access_token": create_access_token({
                "sub": str(admin.id),
                "account_type": "admin"
            }),
            "token_type": "bearer"
        }
    
    customer = get_customer_by_email(db, email)

    if customer and verify_password(password, customer.password):
        return {
            "access_token": create_access_token({
                "sub": str(customer.id),
                "account_type": "customer"
            }),
            "token_type": "bearer"
        }
    company_admin = get_insurance_company_by_email(db, email)
    company_admin_by_phone = get_insurance_company_by_phone_number(db, password)

    if company_admin and company_admin_by_phone:
        return {
            "access_token": create_access_token({
                "sub": str(company_admin.id),
                "account_type": "company_admin"
            }),
            "token_type": "bearer"
        }


    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )