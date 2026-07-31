from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
import uuid
from repositories.quotes_repo import (
    create_quote as repo_create_quote,
    create_quote_batch as repo_create_quote_batch,
    get_all_quotes_by_company as repo_get_all_quotes_by_company,
    get_quote as repo_get_quote,
    update_quote as repo_update_quote,
    delete_quote as repo_delete_quote,
    get_quote_with_details as repo_get_quote_with_details,
)
from database import get_db
from schemas.quotes_schema import *
from security.dependencies import company_admin_required, assert_company_owns


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quotes", tags=["insurance company quotes"])


@router.post("/companies/{company_id}/create")
def create_quote(
    company_id: uuid.UUID,
    quote: quoteCreateInterface,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    assert_company_owns(company_id, current_user)
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
    assert_company_owns(company_id, current_user)
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
    assert_company_owns(company_id, current_user)
    try:
        quotes = repo_get_all_quotes_by_company(db, company_id)
        return quotes
    except Exception as e:
        logger.error(f"Error fetching all quotes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/companies/{company_id}/quotes")
def get_all_quotes_by_company_endpoint(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    assert_company_owns(company_id, current_user)
    try:
        quotes = repo_get_all_quotes_by_company(db, company_id)
        print(f"quotes: {quotes}")
        return quotes
    except Exception as e:
        logger.error(f"Error fetching all quotes for company {company_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/details/{quote_id}")
def get_quote_with_details_endpoint(
    quote_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        quote = repo_get_quote_with_details(db, quote_id)
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        assert_company_owns(quote.insurance_company_id, current_user)
        return quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quote with details {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{quote_id}")
def get_quote_endpoint(
    quote_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        quote = repo_get_quote(db, quote_id)
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        assert_company_owns(quote.insurance_company_id, current_user)
        return quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quote {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{quote_id}")
def update_quote_endpoint(
    quote_id: str,
    quote: quoteUpdateInterface,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        existing = repo_get_quote(db, uuid.UUID(quote_id))
        if not existing:
            raise HTTPException(status_code=404, detail="Quote not found")
        assert_company_owns(existing.insurance_company_id, current_user)
        updated_quote = repo_update_quote(db, quote, uuid.UUID(quote_id))
        if not updated_quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        return updated_quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating quote {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{quote_id}")
def update_quote_request_endpoint(
    quote_id: str,
    quote_request_update: quoteUpdateInterface,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        existing = repo_get_quote(db, uuid.UUID(quote_id))
        if not existing:
            raise HTTPException(status_code=404, detail="Quote not found")
        assert_company_owns(existing.insurance_company_id, current_user)
        updated_quote = repo_update_quote(db, quote_request_update, uuid.UUID(quote_id))
        if not updated_quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        return updated_quote
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating quote request {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{quote_id}")
def delete_quote_endpoint(
    quote_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required)
):
    try:
        existing = repo_get_quote(db, uuid.UUID(quote_id))
        if not existing:
            raise HTTPException(status_code=404, detail="Quote not found")
        assert_company_owns(existing.insurance_company_id, current_user)
        success = repo_delete_quote(db, uuid.UUID(quote_id))
        if not success:
            raise HTTPException(status_code=404, detail="Quote not found")
        return {"detail": "Quote deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting quote {quote_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
