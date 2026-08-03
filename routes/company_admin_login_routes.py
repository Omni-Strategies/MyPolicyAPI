from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import logging

from security.auth import create_access_token
from database import get_db
from models.models import *
from schemas import insurance_company_schema
from sqlalchemy.orm import Session
from security.dependencies import *
from repositories.insurance_company_repo import *
from redis_client import redis_client
from otp_utils import generate_otp, hash_otp, OTP_TTL_SECONDS, MAX_ATTEMPTS
from otp_delivery import send_otp_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/company-login", tags=["company_admin_login"])

COOLDOWN_SECONDS = 30
class RequestOTPRequest(BaseModel):
    email: str
    phone_number: str


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str



@router.post("/request-otp")
def request_otp(request: RequestOTPRequest, db: Session = Depends(get_db)):
    phone_number = "233" + str(request.phone_number).removeprefix("0")
    print(f"Requesting OTP for email: {request.email}, phone number: {phone_number}")
    company_admin = get_insurance_company_by_email_and_phone(db, request.email, phone_number)

    if not company_admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cooldown_key = f"otp_cooldown:{company_admin.id}"
    if redis_client.exists(cooldown_key):
        ttl = redis_client.ttl(cooldown_key)
        raise HTTPException(
            status_code=429,
            detail=f"Please wait {ttl} seconds before requesting another code"
        )

    otp = generate_otp()
    key = f"otp:{company_admin.id}"

    redis_client.hset(key, mapping={"otp_hash": hash_otp(otp), "attempts": 0})
    redis_client.expire(key, OTP_TTL_SECONDS)
    redis_client.set(cooldown_key, "1", ex=COOLDOWN_SECONDS)
    send_otp_email(request.email, otp)

    return {"message": "OTP sent via email"}


@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    company_admin = get_insurance_company_by_phone_number(db, request.phone_number)
    if not company_admin:
        phone_number = "233" + str(request.phone_number).removeprefix("0")
        company_admin = get_insurance_company_by_phone_number(db, phone_number)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    key = f"otp:{company_admin.id}"
    record = redis_client.hgetall(key)

    if not record:
        raise HTTPException(status_code=401, detail="No active OTP request or it has expired")

    attempts = int(record["attempts"])
    if attempts >= MAX_ATTEMPTS:
        redis_client.delete(key)
        raise HTTPException(status_code=429, detail="Too many attempts")

    if record["otp_hash"] != hash_otp(request.otp):
        redis_client.hincrby(key, "attempts", 1)
        raise HTTPException(status_code=401, detail="Invalid OTP")

    redis_client.delete(key)

    return {
        "access_token": create_access_token({
            "sub": str(company_admin.id),
            "account_type": "company_admin"
        }),
        "token_type": "bearer"
    }