# s3_client.py
import base64
import logging
import mimetypes
import uuid
from typing import Optional, Union

import boto3
from botocore.exceptions import ClientError

from config import settings
from schemas.insurance_company_schema import LogoData

logger = logging.getLogger(__name__)

s3 = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name="us-east-1",
)

_bucket_ready = False


def _strip_data_url_prefix(value: str) -> str:
    if "," in value and value.startswith("data:"):
        return value.split(",", 1)[1]
    return value


def public_object_url(key: str) -> str:
    base = settings.S3_PUBLIC_ENDPOINT_URL.rstrip("/")
    bucket = settings.S3_BUCKET.strip("/")
    object_key = key.lstrip("/")
    return f"{base}/{bucket}/{object_key}"


def ensure_bucket() -> None:
    global _bucket_ready
    if _bucket_ready:
        return

    bucket = settings.S3_BUCKET
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError:
        logger.info(f"Creating S3 bucket: {bucket}")
        s3.create_bucket(Bucket=bucket)
        try:
            s3.put_bucket_policy(
                Bucket=bucket,
                Policy=f"""{{
                  "Version": "2012-10-17",
                  "Statement": [{{
                    "Effect": "Allow",
                    "Principal": {{"AWS": ["*"]}},
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::{bucket}/*"]
                  }}]
                }}""",
            )
        except ClientError as e:
            logger.warning(f"Could not set public-read policy on {bucket}: {e}")

    _bucket_ready = True


def upload_logo(
    logo: Union[LogoData, dict, str, None],
    *,
    prefix: str = "logos/insurance-companies",
) -> Optional[str]:
    """Upload LogoData to S3 and return the public URL. Pass through existing URL/key strings."""
    if logo is None:
        return None

    if isinstance(logo, str):
        if logo.startswith("http://") or logo.startswith("https://"):
            return logo
        return public_object_url(logo)

    if hasattr(logo, "dict"):
        logo = logo.dict()

    if not isinstance(logo, dict):
        raise ValueError("Invalid logo payload")

    file_name = logo.get("fileName") or f"{uuid.uuid4()}.bin"
    raw_b64 = logo.get("base64")
    if not raw_b64:
        raise ValueError("Logo base64 content is required")

    try:
        file_bytes = base64.b64decode(_strip_data_url_prefix(raw_b64), validate=False)
    except Exception as e:
        logger.error(f"Failed to decode logo base64: {e}")
        raise ValueError("Invalid logo base64 content") from e

    ensure_bucket()

    safe_name = file_name.replace("/", "_")
    key = f"{prefix}/{uuid.uuid4()}_{safe_name}"
    content_type = mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )
    url = public_object_url(key)
    logger.info(f"Uploaded logo to {url}")
    return url
