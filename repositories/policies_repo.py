from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from models.models import Base, Quotes, InsuranceRequests, InsuranceRequests, InsuranceCompanies, Policies, Customers 
from schemas import form_requests_schema, quotes_schema, requests_schema
import uuid
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

def make_request_status_to_paid(session: Session, request_id: uuid.UUID) -> InsuranceRequests:
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


def make_request_into_policy(session: Session, request_id: uuid.UUID) -> Policies:
    try:
        logger.info(f"[make_request_into_policy] Starting policy creation for request_id: {request_id}")
        
        request = session.query(InsuranceRequests).filter(InsuranceRequests.id == request_id).first()
        logger.info(f"[make_request_into_policy] Insurance request query result: {request}")
        
        if not request:
            logger.warning(f"[make_request_into_policy] No insurance request found with ID: {request_id}")
            return None
            
        quote = session.query(Quotes).filter(Quotes.insurance_request_id == request.id).first()
        logger.info(f"[make_request_into_policy] Quote query result: {quote}")
        
        if not quote:
            logger.warning(f"[make_request_into_policy] No quote found for request ID: {request_id}")
            return None
            
        company = session.query(InsuranceCompanies).filter(InsuranceCompanies.id == quote.insurance_company_id).first()
        logger.info(f"[make_request_into_policy] Insurance company query result: {company}")
        
        if not company:
            logger.warning(f"[make_request_into_policy] No insurance company found with ID: {quote.insurance_company_id}")
            return None
            
        customer = session.query(Customers).filter(Customers.id == request.requested_by).first()
        logger.info(f"[make_request_into_policy] Customer query result: {customer}")
        
        if not customer:
            logger.warning(f"[make_request_into_policy] No customer found with ID: {request.requested_by}")
            return None

        logger.info(f"[make_request_into_policy] All related records found. Processing dates...")
        start_date_str = request.request_data["policy"]["startDate"]
        duration_str = request.request_data["policy"]["duration"]
        logger.info(f"[make_request_into_policy] Start date: {start_date_str}, Duration: {duration_str}")
        
        # Parse start_date string (format: "2026-04-18") and add duration (months)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        duration_months = int(duration_str)
        end_date = start_date + relativedelta(months=duration_months)
        logger.info(f"[make_request_into_policy] Calculated dates - Start: {start_date}, End: {end_date}")

        policy = Policies(
            quote_id=quote.id,
            insurance_company_id=company.id,
            insurance_request_id=request.id,
            created_by=customer.id,
            start_date=start_date,
            end_date=end_date
        )
        
        logger.info(f"[make_request_into_policy] Policy object created: quote_id={quote.id}, company_id={company.id}, request_id={request.id}, customer_id={customer.id}")

        session.add(policy)
        session.commit()
        logger.info(f"[make_request_into_policy] Policy committed to database. Policy ID: {policy.id}")

        return policy
    except Exception as e:
        logger.error(f"[make_request_into_policy] Error occurred while creating policy: {e}", exc_info=True)
        session.rollback()
        raise


def get_policy_and_customer_id(session: Session, policy_id: uuid.UUID) -> tuple[Optional[Policies], Optional[uuid.UUID]]:
    try:
        logger.info(f"[get_policy_and_customer_id] Fetching policy with ID: {policy_id}")
        policy = session.query(Policies).filter(Policies.id == policy_id).first()
        
        if not policy:
            logger.warning(f"[get_policy_and_customer_id] No policy found with ID: {policy_id}")
            return None, None
        
        customer_id = policy.created_by
        logger.info(f"[get_policy_and_customer_id] Policy found with customer_id: {customer_id}")
        
        return policy, customer_id
    except Exception as e:
        logger.error(f"[get_policy_and_customer_id] Error occurred while fetching policy {policy_id}: {e}", exc_info=True)
        raise


def get_policy(session: Session, policy_id: uuid.UUID) -> Optional[Policies]:
    try:
        logger.info(f"[get_policy] Fetching policy with ID: {policy_id}")
        policy = (
            session.query(Policies)
            .options(
                joinedload(Policies.quote)
                .joinedload(Quotes.insurance_request)
                .joinedload(InsuranceRequests.customers),
                joinedload(Policies.insurance_company),
                joinedload(Policies.insurance_request),
                joinedload(Policies.customers),
                joinedload(Policies.policy_documents),
            )
            .filter(Policies.id == policy_id)
            .first()
        )

        if policy:
            logger.info(f"[get_policy] Policy fetched: {policy_id}")
        else:
            logger.warning(f"[get_policy] No policy found with ID: {policy_id}")

        return policy
    except Exception as e:
        logger.error(f"[get_policy] Error occurred while fetching policy {policy_id}: {e}", exc_info=True)
        session.rollback()
        raise


def get_policies_by_company(session: Session, company_id: uuid.UUID) -> list[Policies]:
    try:
        logger.info(f"[get_policies_by_company] Fetching policies for company ID: {company_id}")
        policies = (
            session.query(Policies)
            .options(
                joinedload(Policies.insurance_request)
                .joinedload(InsuranceRequests.customers),
                joinedload(Policies.quote),
                joinedload(Policies.policy_documents),
                joinedload(Policies.customers),
            )
            .filter(Policies.insurance_company_id == company_id)
            .all()
        )
        logger.info(f"[get_policies_by_company] Fetched {len(policies)} policies for company {company_id}")
        return policies
    except Exception as e:
        logger.error(f"[get_policies_by_company] Error fetching policies for company {company_id}: {e}", exc_info=True)
        session.rollback()
        raise


def get_policy_by_company(session: Session, company_id: uuid.UUID, policy_id: uuid.UUID) -> Optional[Policies]:
    try:
        logger.info(f"[get_policy_by_company] Fetching policy {policy_id} for company ID: {company_id}")
        policy = (
            session.query(Policies)
            .options(
                joinedload(Policies.insurance_request)
                .joinedload(InsuranceRequests.customers),
                joinedload(Policies.quote),
                joinedload(Policies.policy_documents),
                joinedload(Policies.customers),
            )
            .filter(Policies.insurance_company_id == company_id)
            .filter(Policies.id == policy_id)
            .first()
        )
        if policy:
            logger.info(f"[get_policy_by_company] Policy found: {policy_id}")
        else:
            logger.warning(f"[get_policy_by_company] No policy {policy_id} for company {company_id}")
        return policy
    except Exception as e:
        logger.error(f"[get_policy_by_company] Error fetching policy {policy_id} for company {company_id}: {e}", exc_info=True)
        session.rollback()
        raise

def delete_policy(session: Session, policy_id: uuid.UUID) -> bool:
    try:
        db_policy = session.query(Policies).filter(Policies.id == policy_id).first()
        if not db_policy:
            return False
        session.delete(db_policy)
        session.commit()
        logger.info(f"Quote deleted with ID: {policy_id}")
        return True
    except Exception as e:
        logger.error(f"Error occurred while deleting quote: {e}")
        session.rollback()
        raise