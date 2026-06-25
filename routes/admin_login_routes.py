from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from security.password import verify_password
from security.auth import create_access_token
from repositories.admin_repo import get_admin_by_email

router = APIRouter(
    prefix="/auth/admin",
    tags=["Admin Authentication"]
)

@router.post("/login")
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    admin = get_admin_by_email(
        db,
        email
    )

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        password,
        admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(admin.id),
            "account_type": "admin"
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "account_type": "admin"
    }