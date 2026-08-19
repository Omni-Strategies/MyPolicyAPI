# otp_delivery.py
import logging

import requests

from config import settings
from otp_utils import OTP_TTL_SECONDS, generate_otp

logger = logging.getLogger(__name__)

WIGAL_OTP_GENERATE_URL = f"{settings.WIGAL_BASE_URL.rstrip('/')}/api/v3/sms/otp/generate"
WIGAL_OTP_VERIFY_URL = f"{settings.WIGAL_BASE_URL.rstrip('/')}/api/v3/sms/otp/verify"
OTP_EXPIRY_MINUTES = max(1, OTP_TTL_SECONDS // 60)


def normalize_phone(phone_number: str) -> str:
    """Normalize to Ghana local format (e.g. 0596032773). Wigal rejects country codes."""
    digits = "".join(ch for ch in (phone_number or "") if ch.isdigit())
    if digits.startswith("233"):
        digits = digits[3:]
    if len(digits) == 9:
        digits = "0" + digits
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


def _local_destination(phone_number: str) -> str:
    destination = normalize_phone(phone_number)
    if not (destination.startswith("0") and len(destination) == 10):
        raise RuntimeError("Invalid Ghana phone number for SMS")
    return destination


def _wigal_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "USERNAME": settings.WIGAL_USERNAME.strip(),
        "API-KEY": settings.WIGAL_API_KEY.strip(),
    }


def _wigal_post(url: str, payload: dict) -> tuple[int, dict]:
    response = requests.post(url, json=payload, headers=_wigal_headers(), timeout=30)
    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}
    return response.status_code, data


def request_otp_sms(phone_number: str) -> str | None:
    """Ask Wigal to generate and SMS an OTP. Returns the code only in mock mode."""
    destination = _local_destination(phone_number)

    if settings.WIGAL_SMS_MOCK:
        otp = generate_otp()
        logger.warning(f"[WIGAL_SMS_MOCK] OTP for {destination}: {otp}")
        return otp

    payload = {
        "number": destination,
        "expiry": OTP_EXPIRY_MINUTES,
        "length": 6,
        "messagetemplate": (
            "Your MyPolicy admin login code is %OTPCODE%. "
            "It expires in %EXPIRY% minutes."
        ),
        "type": "NUMERIC",
        "senderid": settings.WIGAL_SENDER_ID,
    }

    try:
        status_code, data = _wigal_post(WIGAL_OTP_GENERATE_URL, payload)
    except requests.RequestException as e:
        logger.error(f"Failed to reach Wigal OTP generate for {destination}: {e}")
        raise

    if status_code != 200 or str(data.get("status", "")).upper() != "SUCCESS":
        logger.error(
            f"Wigal OTP generate failed for {destination}: HTTP {status_code} {data}"
        )
        raise RuntimeError(data.get("message") or "Failed to send OTP SMS")
    return None


def verify_otp_sms(phone_number: str, otp: str) -> None:
    """Verify an OTP with Wigal. Raises RuntimeError if it is invalid or expired."""
    destination = _local_destination(phone_number)
    payload = {"otpcode": otp, "number": destination}

    try:
        status_code, data = _wigal_post(WIGAL_OTP_VERIFY_URL, payload)
    except requests.RequestException as e:
        logger.error(f"Failed to reach Wigal OTP verify for {destination}: {e}")
        raise

    status = str(data.get("status", "")).upper()
    if status_code == 200 and status not in {"ERROR", "FAILED"}:
        return

    logger.error(f"Wigal OTP verify failed for {destination}: HTTP {status_code} {data}")
    if status_code == 408:
        raise RuntimeError("OTP expired or not found")
    raise RuntimeError(data.get("message") or "OTP verification failed")
