# otp_delivery.py
import logging
import uuid

import requests

from config import settings

logger = logging.getLogger(__name__)

WIGAL_SEND_URL = f"{settings.WIGAL_BASE_URL.rstrip('/')}/api/v3/sms/send"


def send_otp_sms(phone_number: str, otp: str):
    message = f"Your MyPolicy admin login code is {otp}. It expires in 5 minutes."
    payload = {
        "senderid": settings.WIGAL_SENDER_ID,
        "destinations": [
            {
                "destination": phone_number,
                "message": message,
                "msgid": str(uuid.uuid4()),
                "smstype": "text",
            }
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "USERNAME": settings.WIGAL_USERNAME,
        "API-KEY": settings.WIGAL_API_KEY,
    }

    try:
        response = requests.post(WIGAL_SEND_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ACCEPTD":
            logger.error(f"Wigal SMS rejected for {phone_number}: {data}")
            raise RuntimeError(data.get("message") or "Failed to send OTP SMS")
    except requests.RequestException as e:
        logger.error(f"Failed to send OTP SMS to {phone_number}: {e}")
        raise
