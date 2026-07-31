from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from models.models import Quotes, InsuranceRequests, InsuranceCompanies, Policies, Customers
import uuid
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


def _policy_with_documents_query(session: Session):
    return session.query(Policies).options(joinedload(Policies.policy_documents))


def make_request_status_to_paid(session: Session, request_id: uuid.UUID) -> Optional[InsuranceRequests]:
    try:
        logger.info(f"[make_request_status_to_paid] Starting with request_id: {request_id}")
        request = session.query(InsuranceRequests).filter(InsuranceRequests.id == request_id).first()
        logger.info(f"[make_request_status_to_paid] Query result - request: {request}")

        if not request:
            logger.warning(f"[make_request_status_to_paid] No insurance request found with ID: {request_id}")
            return None

        logger.info(f"[make_request_status_to_paid] Setting request status to 'paid'")
        request.status = "paid"

        session.commit()
        logger.info(f"[make_request_status_to_paid] Insurance request {request_id} status set to paid. Final status: {request.status}")

        return request
    except Exception as e:
        logger.error(f"[make_request_status_to_paid] Error occurred while setting request {request_id} status to paid: {e}", exc_info=True)
        session.rollback()
        raise


def _policy_dates_from_request_data(request_data) -> tuple:
    """Resolve start/end dates from request_data, with safe defaults for testing."""
    data = request_data if isinstance(request_data, dict) else {}
    policy = data.get("policy") if isinstance(data.get("policy"), dict) else {}

    start_date_str = (
        policy.get("startDate")
        or policy.get("start_date")
        or data.get("startDate")
        or data.get("start_date")
    )
    duration_raw = (
        policy.get("duration")
        or data.get("duration")
        or data.get("duration_months")
    )

    if start_date_str:
        start_date = datetime.strptime(str(start_date_str)[:10], "%Y-%m-%d").date()
    else:
        start_date = datetime.utcnow().date()
        logger.warning(
            "[make_request_into_policy] No startDate in request_data; defaulting to today"
        )

    try:
        duration_months = int(duration_raw) if duration_raw is not None else 12
    except (TypeError, ValueError):
        duration_months = 12

    end_date = start_date + relativedelta(months=duration_months)
    return start_date, end_date


def make_request_into_policy(
    session: Session,
    request_id: uuid.UUID,
    quote_id: uuid.UUID,
) -> Optional[Policies]:
    try:
        logger.info(f"[make_request_into_policy] Starting policy creation for request_id: {request_id}, quote_id: {quote_id}")

        request = session.query(InsuranceRequests).filter(InsuranceRequests.id == request_id).first()
        if not request:
            logger.warning(f"[make_request_into_policy] No insurance request found with ID: {request_id}")
            return None

        quote = (
            session.query(Quotes)
            .filter(
                Quotes.id == quote_id,
                Quotes.insurance_request_id == request.id,
            )
            .first()
        )
        if not quote:
            logger.warning(
                f"[make_request_into_policy] No quote {quote_id} found for request ID: {request_id}"
            )
            return None

        company = session.query(InsuranceCompanies).filter(InsuranceCompanies.id == quote.insurance_company_id).first()
        if not company:
            logger.warning(f"[make_request_into_policy] No insurance company found with ID: {quote.insurance_company_id}")
            return None

        customer = session.query(Customers).filter(Customers.id == request.requested_by).first()
        if not customer:
            logger.warning(f"[make_request_into_policy] No customer found with ID: {request.requested_by}")
            return None

        start_date, end_date = _policy_dates_from_request_data(request.request_data)

        policy = Policies(
            quote_id=quote.id,
            insurance_company_id=company.id,
            insurance_request_id=request.id,
            created_by=customer.id,
            start_date=start_date,
            end_date=end_date,
        )

        session.add(policy)
        session.commit()
        session.refresh(policy)
        logger.info(f"[make_request_into_policy] Policy committed to database. Policy ID: {policy.id}")

        return policy
    except Exception as e:
        logger.error(f"[make_request_into_policy] Error occurred while creating policy: {e}", exc_info=True)
        session.rollback()
        raise


def get_policy(session: Session, policy_id: uuid.UUID) -> Optional[Policies]:
    try:
        policy = (
            _policy_with_documents_query(session)
            .filter(Policies.id == policy_id)
            .first()
        )
        if policy:
            logger.info(f"Policy fetched with ID: {policy_id}")
        else:
            logger.warning(f"No policy found with ID: {policy_id}")
        return policy
    except Exception as e:
        logger.error(f"Error fetching policy {policy_id}: {e}")
        session.rollback()
        raise


def get_policies_by_company(session: Session, company_id: uuid.UUID) -> List[Policies]:
    try:
        policies = (
            _policy_with_documents_query(session)
            .filter(Policies.insurance_company_id == company_id)
            .all()
        )
        logger.info(f"Fetched {len(policies)} policies for company {company_id}")
        return policies
    except Exception as e:
        logger.error(f"Error fetching policies for company {company_id}: {e}")
        session.rollback()
        raise


def get_policy_by_company(
    session: Session,
    company_id: uuid.UUID,
    policy_id: uuid.UUID,
) -> Optional[Policies]:
    try:
        policy = (
            _policy_with_documents_query(session)
            .filter(
                Policies.id == policy_id,
                Policies.insurance_company_id == company_id,
            )
            .first()
        )
        if policy:
            logger.info(f"Policy {policy_id} fetched for company {company_id}")
        else:
            logger.warning(f"No policy {policy_id} found for company {company_id}")
        return policy
    except Exception as e:
        logger.error(f"Error fetching policy {policy_id} for company {company_id}: {e}")
        session.rollback()
        raise


def delete_policy(session: Session, policy_id: uuid.UUID) -> bool:
    try:
        policy = session.query(Policies).filter(Policies.id == policy_id).first()
        if not policy:
            logger.warning(f"No policy found with ID: {policy_id}")
            return False
        session.delete(policy)
        session.commit()
        logger.info(f"Policy deleted with ID: {policy_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting policy {policy_id}: {e}")
        session.rollback()
        raise


def get_policy_and_customer_id(
    session: Session,
    policy_id: uuid.UUID,
) -> Optional[Tuple[Policies, uuid.UUID]]:
    try:
        policy = session.query(Policies).filter(Policies.id == policy_id).first()
        if not policy:
            logger.warning(f"No policy found with ID: {policy_id}")
            return None
        return policy, policy.created_by
    except Exception as e:
        logger.error(f"Error fetching policy and customer for {policy_id}: {e}")
        session.rollback()
        raise
