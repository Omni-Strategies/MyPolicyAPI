# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Wigal / SMS OTP
    WIGAL_BASE_URL: str = "https://frogapi.wigal.com.gh"
    WIGAL_USERNAME: str
    WIGAL_API_KEY: str
    WIGAL_SENDER_ID: str
    # When true, skip Wigal and log/return OTP (local/dev only)
    WIGAL_SMS_MOCK: bool = False

    # S3 / MinIO
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_PUBLIC_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "mypolicy-documents"

    class Config:
        env_file = ".env"

settings = Settings()
