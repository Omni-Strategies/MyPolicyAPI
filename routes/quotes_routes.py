from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging
import uuid
from repositories.quotes_repo import (
    create_quote as repo_create_quote,
    create_quote_batch as repo_create_quote_batch,
    get_all_quotes as repo_get_all_quotes,
    get_quote as repo_get_quote,
    update_quote as repo_update_quote,
    delete_quote as repo_delete_quote,
)
from security.password import verify_password
from security.auth import create_access_token
from repositories.requests_repo import *
from database import get_db
from schemas.quotes_schema import *
from security.dependencies import company_admin_required

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quotes", tags=["insurance company quotes"])

@router.post("/companies/{company_id}/create")
def create_quote(
    company_id: uuid.UUID,
    quote: quoteCreateInterface,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        created_quote = repo_create_quote(db, quote, company_id)
        return created_quote
    except Exception as e:
        logger.error(f"Error creating quote: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/companies/{company_id}/create_batch")
def create_quote_batch(
    company_id: uuid.UUID,
    quote_batch: QuoteBatchCreate,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),

):
    try:
        created_quotes = repo_create_quote_batch(db, quote_batch, company_id)
        return created_quotes
    except Exception as e:
        logger.error(f"Error creating quote batch: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/companies/{company_id}/all")
def get_all_quotes_endpoint(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        quotes = repo_get_all_quotes(db, company_id)
        return quotes
    except Exception as e:
        logger.error(f"Error fetching all quotes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/companies/{company_id}/quotes/{quote_id}")
def get_quote_endpoint(
    company_id: uuid.UUID,
    quote_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        quote = repo_get_quote(db, uuid.UUID(quote_id))
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        return quote
    except Exception as e:
        logger.error(f"Error fetching quote {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/companies/{company_id}/quotes/{quote_id}")
def update_quote_endpoint(
    quote_id: str,
    quote: quoteUpdateInterface,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        updated_quote = repo_update_quote(db, quote, uuid.UUID(quote_id))
        if not updated_quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        return updated_quote
    except Exception as e:
        logger.error(f"Error updating quote {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/companies/{company_id}/quotes/{quote_id}")
def delete_quote_endpoint(
    quote_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        success = repo_delete_quote(db, uuid.UUID(quote_id))
        if not success:
            raise HTTPException(status_code=404, detail="Quote not found")
        return {"detail": "Quote deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting quote {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
