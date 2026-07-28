# otp_utils.py
import secrets
import hashlib

OTP_TTL_SECONDS = 300  # 5 minutes
MAX_ATTEMPTS = 3

def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()