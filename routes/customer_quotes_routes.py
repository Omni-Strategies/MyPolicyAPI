from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import uuid

from database import get_db
from repositories.quotes_repo import (
    get_quotes_with_details_by_customer as repo_get_quotes_with_details_by_customer,
)
from security.dependencies import customer_required

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/customer-quotes", tags=["customer quotes"])


@router.get(
    "/",
    summary="List my quotes",
    description="Returns all quotes received for the logged-in customer's insurance requests.",
)
def list_my_quotes(
    db: Session = Depends(get_db),
    current_user=Depends(customer_required),
):
    try:
        customer_id = uuid.UUID(str(current_user["id"]))
        return repo_get_quotes_with_details_by_customer(db, customer_id) or []
    except Exception as e:
        logger.error(
            f"Error listing quotes for customer {current_user.get('id')}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))
