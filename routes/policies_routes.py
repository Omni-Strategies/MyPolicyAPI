from fastapi import UploadFile
from fastapi import APIRouter, HTTPException, Depends
from security.dependencies import *
from database import get_db
from repositories.policies_repo import *
from models.models import InsuranceRequests, Policies, PolicyDocuments
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
    endpoint_url=settings.S3_ENDPOINT_URL,   # internal: http://minio:9000
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name="us-east-1",
)

@router.post("/requests/{policy_id}/documents")
async def upload_document(
    policy_id: uuid.UUID,
    file: UploadFile,
    description: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(company_admin_required)
):
    key = f"policies/{policy_id}/{uuid.uuid4()}_{file.filename}"

    s3.upload_fileobj(file.file, settings.S3_BUCKET, key)
    policy, customer_id = get_policy_and_customer_id(db, policy_id)

    doc = PolicyDocuments(
        policy_id=policy_id,
        created_for=customer_id,
        document_key=key,
        description=description
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "file_key": doc.document_key}

@router.get("/requests/{policy_id}/documents/{document_id}")
async def download_document(
    policy_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(company_admin_required)
):
    doc = db.query(PolicyDocuments).filter(
        PolicyDocuments.id == document_id,
        PolicyDocuments.policy_id == policy_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    s3_object = s3.get_object(Bucket=settings.S3_BUCKET, Key=doc.document_key)

    filename = doc.document_key.split("/")[-1]

    return StreamingResponse(
        s3_object["Body"],
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.post("/create")
async def create_policy(    
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(customer_required)):
    try:
        logger.info(f"Starting policy creation for request_id: {request_id}")
        logger.info(f"Current user: {current_user}")
        
        # First mark the request as paid
        logger.info(f"Attempting to mark request {request_id} as paid")
        paid_request = make_request_status_to_paid(db, request_id)
        logger.info(f"Result of make_request_status_to_paid: {paid_request}")
        
        if not paid_request:
            logger.warning(f"Insurance request not found for ID: {request_id}")
            raise HTTPException(status_code=404, detail="Insurance request not found")
        
        logger.info(f"Request found with status: {paid_request.status}")
        
        if paid_request.status != "paid":
            logger.warning(f"Request status is {paid_request.status}, not 'paid'")
            raise HTTPException(status_code=400, detail="Failed to mark request as paid")
        
        # Create the policy from the paid request
        logger.info(f"Creating policy from paid request {request_id}")
        policy = make_request_into_policy(db, request_id)
        logger.info(f"Policy creation result: {policy}")
        
        if not policy:
            logger.error(f"Failed to create policy for request {request_id}")
            raise HTTPException(status_code=500, detail="Failed to create policy")
        
        logger.info(f"Policy successfully created with ID: {policy.id}")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating policy: {str(e)}", exc_info=True)
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

        # If requester is a customer, ensure they own the policy
        if current_user["account_type"] == "customer":
            if str(policy.created_by) != current_user["id"]:
                raise HTTPException(status_code=403, detail="Not authorized to view this policy")

        return policy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching policy {policy_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companies/{company_id}/all")
def get_policies_by_company_route(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        policies = get_policies_by_company(db, company_id)
        return policies
    except Exception as e:
        logger.error(f"Error fetching policies for company {company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companies/{company_id}/{policy_id}")
def get_policy_by_company_route(
    company_id: uuid.UUID,
    policy_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        policy = get_policy_by_company(db, company_id, policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found for this company")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching policy {policy_id} for company {company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{policy_id}")
def delete_policy_endpoint(
    policy_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        success = delete_policy(db, uuid.UUID(policy_id))
        if not success:
            raise HTTPException(status_code=404, detail="Policy not found")
        return {"detail": "Policy deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting policy {policy_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/requests/{policy_id}/documents/{document_id}")
async def delete_document(
    policy_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(company_admin_required)
):
    doc = db.query(PolicyDocuments).filter(
        PolicyDocuments.id == document_id,
        PolicyDocuments.policy_id == policy_id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        s3.delete_object(Bucket=settings.S3_BUCKET, Key=doc.document_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete file from storage")

    db.delete(doc)
    db.commit()

    return {"detail": "Document deleted"}