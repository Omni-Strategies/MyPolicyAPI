from fastapi import UploadFile
from fastapi import APIRouter, HTTPException, Depends
from security.dependencies import *
from database import get_db
from repositories.policies_repo import *
from repositories.requests_repo import get_request
from models.models import PolicyDocuments
from config import settings
import uuid
from sqlalchemy.orm import Session
import logging
import boto3
from fastapi.responses import StreamingResponse


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/policies", tags=["Policies"])

s3 = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name="us-east-1",
)


def _serialize_policy_document(doc: PolicyDocuments) -> dict:
    key = doc.document_key or ""
    filename = key.rsplit("/", 1)[-1]
    # Keys are stored as policies/{id}/{uuid}_{original_filename}
    if "_" in filename:
        filename = filename.split("_", 1)[1]
    return {
        "id": doc.id,
        "description": doc.description,
        "document_key": doc.document_key,
        "file_name": filename or None,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
        "deleted": doc.deleted,
    }


def _serialize_policy(policy) -> dict:
    documents = [
        _serialize_policy_document(doc)
        for doc in (policy.policy_documents or [])
        if not doc.deleted
    ]
    return {
        "id": policy.id,
        "status": policy.status,
        "start_date": policy.start_date,
        "end_date": policy.end_date,
        "created_at": policy.created_at,
        "quote_id": policy.quote_id,
        "insurance_company_id": policy.insurance_company_id,
        "insurance_request_id": policy.insurance_request_id,
        "created_by": policy.created_by,
        "deleted": policy.deleted,
        "policy_documents": documents,
    }


def _require_company_owns_policy(db: Session, policy_id: uuid.UUID, current_user: dict):
    policy = get_policy(db, policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    assert_company_owns(policy.insurance_company_id, current_user)
    return policy


@router.post("/requests/{policy_id}/documents")
async def upload_document(
    policy_id: uuid.UUID,
    file: UploadFile,
    description: str,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    _require_company_owns_policy(db, policy_id, current_user)

    result = get_policy_and_customer_id(db, policy_id)
    if not result:
        raise HTTPException(status_code=404, detail="Policy not found")
    policy, customer_id = result

    key = f"policies/{policy_id}/{uuid.uuid4()}_{file.filename}"
    s3.upload_fileobj(file.file, settings.S3_BUCKET, key)

    doc = PolicyDocuments(
        policy_id=policy_id,
        created_for=customer_id,
        document_key=key,
        description=description,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _serialize_policy_document(doc)


@router.get("/requests/{policy_id}/documents/{document_id}")
async def download_document(
    policy_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    _require_company_owns_policy(db, policy_id, current_user)

    doc = db.query(PolicyDocuments).filter(
        PolicyDocuments.id == document_id,
        PolicyDocuments.policy_id == policy_id,
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    s3_object = s3.get_object(Bucket=settings.S3_BUCKET, Key=doc.document_key)
    filename = doc.document_key.split("/")[-1]

    return StreamingResponse(
        s3_object["Body"],
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/create")
async def create_policy(
    request_id: uuid.UUID,
    quote_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(customer_required),
):
    try:
        logger.info(f"Starting policy creation for request_id: {request_id}, quote_id: {quote_id}")

        request = get_request(db, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Insurance request not found")
        if str(request.requested_by) != str(current_user["id"]):
            raise HTTPException(status_code=403, detail="Not authorized for this request")

        paid_request = make_request_status_to_paid(db, request_id)
        if not paid_request or paid_request.status != "paid":
            raise HTTPException(status_code=400, detail="Failed to mark request as paid")

        policy = make_request_into_policy(db, request_id, quote_id)
        if not policy:
            raise HTTPException(
                status_code=400,
                detail="Failed to create policy; quote must belong to this request",
            )

        logger.info(f"Policy successfully created with ID: {policy.id}")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating policy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companies/{company_id}/all")
def get_policies_by_company_route(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    assert_company_owns(company_id, current_user)
    try:
        return [_serialize_policy(policy) for policy in get_policies_by_company(db, company_id)]
    except Exception as e:
        logger.error(f"Error fetching policies for company {company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companies/{company_id}/{policy_id}")
def get_policy_by_company_route(
    company_id: uuid.UUID,
    policy_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    assert_company_owns(company_id, current_user)
    try:
        policy = get_policy_by_company(db, company_id, policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found for this company")
        return _serialize_policy(policy)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching policy {policy_id} for company {company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{policy_id}")
async def get_policy_route(
    policy_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("customer", "company_admin")),
):
    try:
        policy = get_policy(db, policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")

        if current_user["account_type"] == "customer":
            if str(policy.created_by) != current_user["id"]:
                raise HTTPException(status_code=403, detail="Not authorized to view this policy")
        elif current_user["account_type"] == "company_admin":
            assert_company_owns(policy.insurance_company_id, current_user)

        return _serialize_policy(policy)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching policy {policy_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{policy_id}")
def delete_policy_endpoint(
    policy_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    try:
        policy = get_policy(db, uuid.UUID(policy_id))
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        assert_company_owns(policy.insurance_company_id, current_user)

        success = delete_policy(db, uuid.UUID(policy_id))
        if not success:
            raise HTTPException(status_code=404, detail="Policy not found")
        return {"detail": "Policy deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting policy {policy_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/requests/{policy_id}/documents/{document_id}")
async def delete_document(
    policy_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    _require_company_owns_policy(db, policy_id, current_user)

    doc = db.query(PolicyDocuments).filter(
        PolicyDocuments.id == document_id,
        PolicyDocuments.policy_id == policy_id,
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        s3.delete_object(Bucket=settings.S3_BUCKET, Key=doc.document_key)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete file from storage")

    db.delete(doc)
    db.commit()

    return {"detail": "Document deleted"}
