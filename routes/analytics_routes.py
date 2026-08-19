from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
import uuid

from database import get_db
from repositories.analytics_repo import get_company_analytics_report
from schemas.analytics_schema import CompanyAnalyticsReport
from security.dependencies import company_admin_required, assert_company_owns

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analytics", tags=["company analytics"])


@router.get(
    "/companies/{company_id}",
    response_model=CompanyAnalyticsReport,
)
def get_company_analytics(
    company_id: uuid.UUID,
    from_date: date | None = Query(None, description="Inclusive start date (YYYY-MM-DD)"),
    to_date: date | None = Query(None, description="Inclusive end date (YYYY-MM-DD)"),
    expiring_within_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user=Depends(company_admin_required),
):
    assert_company_owns(company_id, current_user)
    if from_date and to_date and from_date > to_date:
        raise HTTPException(status_code=400, detail="from_date must be on or before to_date")

    try:
        report = get_company_analytics_report(
            db,
            company_id,
            from_date=from_date,
            to_date=to_date,
            expiring_within_days=expiring_within_days,
        )
    except Exception as e:
        logger.error(f"Error generating analytics for company {company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate analytics report")

    if not report:
        raise HTTPException(status_code=404, detail="Insurance company not found")
    return report
