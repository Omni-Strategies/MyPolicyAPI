from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import logging
from security.auth import create_access_token
from database import get_db
from sqlalchemy.orm import Session
from repositories.insurance_company_repo import (
    get_insurance_company_by_email,
    get_insurance_company_by_phone_number,
)
from redis_client import redis_client
from otp_utils import hash_otp, OTP_TTL_SECONDS, MAX_ATTEMPTS
from otp_delivery import request_otp_sms, verify_otp_sms, normalize_phone
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/company-login", tags=["company_admin_login"])

COOLDOWN_SECONDS = 30


class RequestOTPRequest(BaseModel):
    email: str
    phone_number: str


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str


def _otp_key(phone_number: str) -> str:
    return f"company_otp:{normalize_phone(phone_number)}"


def _cooldown_key(phone_number: str) -> str:
    return f"company_otp_cooldown:{normalize_phone(phone_number)}"


def _phone_matches_stored(request_phone: str, stored_numbers: list) -> bool:
    want = normalize_phone(request_phone)
    return any(normalize_phone(str(p)) == want for p in (stored_numbers or []))


@router.post("/request-otp")
def request_otp(request: RequestOTPRequest, db: Session = Depends(get_db)):
    company_admin = get_insurance_company_by_email(db, request.email)
    if not company_admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    phone = normalize_phone(request.phone_number)
    if not phone or not _phone_matches_stored(phone, company_admin.phone_numbers or []):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cooldown_key = _cooldown_key(phone)
    if redis_client.exists(cooldown_key):
        raise HTTPException(status_code=429, detail="Please wait before requesting another OTP")

    key = _otp_key(phone)

    try:
        otp = request_otp_sms(phone)
    except Exception as e:
        logger.error(f"Failed to send OTP SMS to {phone}: {e}")
        raise HTTPException(status_code=502, detail=str(e) or "Failed to send OTP SMS")

    mapping = {"attempts": 0}
    if otp:
        mapping["otp_hash"] = hash_otp(otp)
    redis_client.hset(key, mapping=mapping)
    redis_client.expire(key, OTP_TTL_SECONDS)
    redis_client.set(cooldown_key, "1", ex=COOLDOWN_SECONDS)

    logger.info(f"OTP requested for {phone}")
    response = {"message": "OTP sent via SMS"}
    if settings.WIGAL_SMS_MOCK and otp:
        response["otp"] = otp  # local/dev only
    return response


@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    phone = normalize_phone(request.phone_number)
    company_admin = get_insurance_company_by_phone_number(db, phone)
    if not company_admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    key = _otp_key(phone)
    stored = redis_client.hgetall(key)
    if not stored:
        raise HTTPException(status_code=400, detail="OTP expired or not found")

    attempts = int(stored.get("attempts", 0))
    if attempts >= MAX_ATTEMPTS:
        redis_client.delete(key)
        raise HTTPException(status_code=400, detail="Too many invalid attempts")

    if settings.WIGAL_SMS_MOCK:
        if hash_otp(request.otp) != stored.get("otp_hash"):
            redis_client.hincrby(key, "attempts", 1)
            raise HTTPException(status_code=400, detail="OTP verification failed")
    else:
        try:
            verify_otp_sms(phone, request.otp)
        except Exception as e:
            redis_client.hincrby(key, "attempts", 1)
            detail = str(e) or "OTP verification failed"
            status = 400 if "expired" in detail.lower() or "verification" in detail.lower() else 502
            raise HTTPException(status_code=status, detail=detail)

    redis_client.delete(key)
    logger.info(f"OTP verified for {phone}")

    return {
        "access_token": create_access_token({
            "sub": str(company_admin.id),
            "account_type": "company_admin"
        }),
        "token_type": "bearer"
    }
