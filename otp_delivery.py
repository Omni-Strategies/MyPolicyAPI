# otp_delivery.py
import smtplib
import logging
from email.mime.text import MIMEText
from config import settings

logger = logging.getLogger(__name__)


def send_otp_email(email: str, otp: str):
    msg = MIMEText(f"Your MyPolicy admin login code is {otp}. It expires in 5 minutes.")
    msg["Subject"] = "Your MyPolicy Admin Login Code"
    msg["From"] = settings.SMTP_FROM_EMAIL
    msg["To"] = email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, [email], msg.as_string())
    except smtplib.SMTPException as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")
        raise