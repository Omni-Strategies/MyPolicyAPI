# otp_delivery.py
import logging
import uuid

import requests

from config import settings

logger = logging.getLogger(__name__)

WIGAL_SEND_URL = f"{settings.WIGAL_BASE_URL.rstrip('/')}/api/v3/sms/send"


def normalize_phone(phone_number: str) -> str:
    """Normalize to Ghana local format (e.g. 0596032773), no +233."""
    digits = "".join(ch for ch in (phone_number or "") if ch.isdigit())
    if digits.startswith("233") and len(digits) == 12:
        return "0" + digits[3:]
    if digits.startswith("0") and len(digits) == 10:
        return digits
    return digits


def phone_lookup_variants(phone_number: str) -> list[str]:
    """Formats that may exist in the DB for the same Ghana number."""
    local = normalize_phone(phone_number)
    if not local:
        return []
    variants = {local, phone_number.strip()}
    if local.startswith("0") and len(local) == 10:
        national = local[1:]
        variants.update({f"233{national}", f"+233{national}"})
    return [v for v in variants if v]


def send_otp_sms(phone_number: str, otp: str) -> None:
    """Deliver a locally generated OTP. When WIGAL_SMS_MOCK is true, only log it."""
    destination = normalize_phone(phone_number)
    message = f"Your MyPolicy admin login code is {otp}. It expires in 5 minutes."

    if settings.WIGAL_SMS_MOCK:
        logger.warning(f"[WIGAL_SMS_MOCK] OTP for {destination}: {otp}")
        return

    payload = {
        "senderid": settings.WIGAL_SENDER_ID,
        "destinations": [
            {
                "destination": destination,
                "message": message,
                "msgid": str(uuid.uuid4()),
                "smstype": "text",
            }
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "USERNAME": settings.WIGAL_USERNAME.strip(),
        "API-KEY": settings.WIGAL_API_KEY,
    }

    try:
        response = requests.post(WIGAL_SEND_URL, json=payload, headers=headers, timeout=30)
        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        if response.status_code != 200 or data.get("status") != "ACCEPTD":
            logger.error(f"Wigal SMS failed for {destination}: HTTP {response.status_code} {data}")
            raise RuntimeError(data.get("message") or "Failed to send OTP SMS")
    except requests.RequestException as e:
        logger.error(f"Failed to send OTP SMS to {destination}: {e}")
        raise
