from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from models.models import Base, Quotes, InsuranceRequests 
from schemas import form_requests_schema, quotes_schema
import uuid
import logging

logger = logging.getLogger(__name__)

def create_quote(session: Session, quote: quotes_schema.quoteCreateInterface, company_id: uuid.UUID) -> Quotes:
    db_quote = Quotes(
        **quote.dict(by_alias=False),
        insurance_company_id=company_id,
        agent_commission=None,
    )
    try:
        session.add(db_quote)
        session.commit()
        session.refresh(db_quote)
        logger.info(f"Quote created with ID: {db_quote.id}")
        return db_quote
    except Exception as e:
        logger.error(f"Error occurred while creating quote: {e}")
        session.rollback()
        raise


def create_quote_batch(session: Session, quote_batch: quotes_schema.QuoteBatchCreate, company_id: uuid.UUID) -> List[Quotes]:
    db_quotes = [
        Quotes(
            **quote.dict(by_alias=False),
            insurance_company_id=company_id,
            agent_commission=None,
        )
        for quote in quote_batch.items
    ]
    try:
        session.add_all(db_quotes)
        session.commit()
        for db_quote in db_quotes:
            session.refresh(db_quote)
        logger.info(f"Batch of {len(db_quotes)} quotes created")
        return db_quotes
    except Exception as e:
        logger.error(f"Error occurred while creating batch of quotes: {e}")
        session.rollback()
        raise
    
def get_all_quotes(session: Session) -> List[Quotes]:
    try:
        quotes = session.query(Quotes).all()
        logger.info(f"Fetched {len(quotes)} quotes")
        return quotes
    except Exception as e:
        logger.error(f"Error occurred while fetching quotes: {e}")
        session.rollback()
        raise
def get_all_quotes_by_company(session: Session, company_id: uuid.UUID) -> List[Quotes]:
    try:
        quotes = (
            session.query(Quotes)
            .options(
                joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.customers),
                joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.insurance_product),
                joinedload(Quotes.insurance_company)
            )
            .filter(Quotes.insurance_company_id == company_id)
            
            .all()
        )
        logger.info(f"Fetched {len(quotes)} quotes for company ID: {company_id}")
        return quotes
    except Exception as e:
        logger.error(f"Error occurred while fetching quotes for company ID {company_id}: {e}")
        session.rollback()
        raise
def get_quote(session: Session, quote_id: uuid.UUID) -> Optional[Quotes]:
    try:
        quote = session.query(Quotes).filter(Quotes.id == quote_id).first()
        if quote:
            logger.info(f"Quote fetched with ID: {quote_id}")
        else:
            logger.warning(f"No quote found with ID: {quote_id}")
        return quote
    except Exception as e:
        logger.error(f"Error occurred while fetching quote: {e}")
        session.rollback()
        raise

def get_quote_with_details(session: Session, quote_id: uuid.UUID) -> Optional[Quotes]:
    try:
        quote = (
            session.query(Quotes)
            .options(
                joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.customers),
                joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.insurance_product),
                joinedload(Quotes.insurance_company)
            )
            .filter(Quotes.id == quote_id)
            .first()
        )
        if quote:
            logger.info(f"Quote with details fetched with ID: {quote_id}")
        else:
            logger.warning(f"No quote found with ID: {quote_id}")
        return quote
    
    except Exception as e:
        logger.error(f"Error occurred while fetching quote with details: {e}")
        session.rollback()
        raise

def get_quotes_with_details_by_customer(session: Session, customer_id: uuid.UUID) -> list[Quotes]:
    try:
        quotes = (
            session.query(Quotes)
            .join(Quotes.insurance_request)
            .options(
                joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.customers),
                joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.insurance_product),
            )
            .filter(InsuranceRequests.requested_by == customer_id)
            .all()
        )
        logger.info(f"Fetched {len(quotes)} quotes for customer: {customer_id}")
        return quotes
    except Exception as e:
        logger.error(f"Error fetching quotes for customer {customer_id}: {e}")
        raise
    

def update_quote(session: Session, quote: quotes_schema.quoteUpdateInterface, quote_id: uuid.UUID) -> Optional[Quotes]:
    try:
        db_quote = session.query(Quotes).filter(Quotes.id == quote_id).first()
        if not db_quote:
            return None
        for key, value in quote.dict(exclude_unset=True).items():
            if hasattr(db_quote, key):
                setattr(db_quote, key, value)
        session.add(db_quote)
        session.commit()
        session.refresh(db_quote)
        return db_quote
    except Exception as e:
        logger.error(f"Error occurred while updating quote: {e}")
        session.rollback()
        raise

def delete_quote(session: Session, quote_id: uuid.UUID) -> bool:
    try:
        db_quote = session.query(Quotes).filter(Quotes.id == quote_id).first()
        if not db_quote:
            return False
        session.delete(db_quote)
        session.commit()
        logger.info(f"Quote deleted with ID: {quote_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting quote: {e}")
        session.rollback()
        raise
