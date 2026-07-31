from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import logging
import requests
import json
import os
from security.auth import create_access_token
from database import get_db
from models.models import *
from schemas import insurance_company_schema
from sqlalchemy.orm import Session
from security.dependencies import *
from repositories.insurance_company_repo import *

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/company-login", tags=["company_admin_login"])


class RequestOTPRequest(BaseModel):
    email: str
    phone_number: str


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str


@router.post("/request-otp")
def request_otp(request: RequestOTPRequest, db: Session = Depends(get_db)):
    company_admin = get_insurance_company_by_email(db, request.email)

    if not company_admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_numbers = [str(p) for p in (company_admin.phone_numbers or [])]
    if str(request.phone_number) not in stored_numbers:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    post_data = {
        "number": request.phone_number,
        "expiry": 1,
        "length": 6,
        "messagetemplate": "Hello, your OTP is : %OTPCODE%. It will expire after %EXPIRY% mins",
        "type": "ALPHANUMERIC",
        "senderid": os.getenv("WIGAL_SENDER_ID"),
    }

    headers = {
        "Content-Type": "application/json",
        "API-KEY": os.getenv("WIGAL_KEY"),
        "USERNAME": os.getenv("WIGAL_USERNAME"),
    }

    try:
        response = requests.post(
            "https://frogapi.wigal.com.gh/api/v3/sms/otp/generate",
            headers=headers,
            data=json.dumps(post_data),
            timeout=10,
        )
    except requests.RequestException as e:
        logger.error(f"Wigal OTP request failed: {e}")
        raise HTTPException(status_code=502, detail="Failed to reach OTP provider")

    print(f"[request_otp] status: {response.status_code}")

    if response.status_code != 200:
        logger.error(
            f"Wigal OTP generate failed [{response.status_code}]: {response.text}"
        )
        raise HTTPException(status_code=502, detail="OTP provider error")

    data = response.json()
    logger.info(f"OTP requested for {request.phone_number}")
    return data


@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    company_admin = get_insurance_company_by_phone_number(db, request.phone_number)
    post_data = {
        "otpcode": request.otp,
        "number": request.phone_number,
    }

    headers = {
        "Content-Type": "application/json",
        "API-KEY": os.getenv("WIGAL_KEY"),
        "USERNAME": os.getenv("WIGAL_USERNAME"),
    }

    try:
        response = requests.post(
            "https://frogapi.wigal.com.gh/api/v3/sms/otp/verify",
            headers=headers,
            data=json.dumps(post_data),
            timeout=10,
        )
    except requests.RequestException as e:
        logger.error(f"Wigal OTP verify failed: {e}")
        raise HTTPException(status_code=502, detail="Failed to reach OTP provider")

    print(f"[verify_otp] status: {response.status_code}")

    if response.status_code != 200:
        logger.error(
            f"Wigal OTP verify failed [{response.status_code}]: {response.text}"
        )
        raise HTTPException(status_code=400, detail="OTP verification failed")

    data = response.json()
    logger.info(f"OTP verified for {request.phone_number}")

    return {
        "access_token": create_access_token({
            "sub": str(company_admin.id),
            "account_type": "company_admin"
        }),
        "token_type": "bearer"
    }
