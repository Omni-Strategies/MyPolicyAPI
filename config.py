# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # SMTP / Email OTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    # S3 / MinIO
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_PUBLIC_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "mypolicy-documents"

    class Config:
        env_file = ".env"

settings = Settings()