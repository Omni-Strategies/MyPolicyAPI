from datetime import date, timedelta
from typing import Optional
import uuid
import logging

from sqlalchemy import and_, cast, Date, func
from sqlalchemy.orm import Session

from models.models import (
    InsuranceCompanies,
    InsuranceProducts,
    InsuranceRequests,
    Payments,
    Policies,
    PolicyDocuments,
    Quotes,
)

logger = logging.getLogger(__name__)


def _money(value) -> float:
    if value is None:
        return 0.0
    return round(float(value), 2)


def _not_deleted(column):
    return column.is_not(True)


def _in_date_range(column, from_date: Optional[date], to_date: Optional[date]):
    filters = []
    if from_date:
        filters.append(cast(column, Date) >= from_date)
    if to_date:
        filters.append(cast(column, Date) <= to_date)
    return filters


def _counts_by(session: Session, model, group_col, company_id, date_col, from_date, to_date):
    query = (
        session.query(group_col, func.count(model.id))
        .filter(model.insurance_company_id == company_id)
        .filter(_not_deleted(model.deleted))
    )
    for clause in _in_date_range(date_col, from_date, to_date):
        query = query.filter(clause)
    return {status or "unknown": count for status, count in query.group_by(group_col).all()}


def get_company_analytics_report(
    session: Session,
    company_id: uuid.UUID,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    expiring_within_days: int = 30,
) -> Optional[dict]:
    company = (
        session.query(InsuranceCompanies)
        .filter(InsuranceCompanies.id == company_id)
        .filter(_not_deleted(InsuranceCompanies.deleted))
        .first()
    )
    if not company:
        return None

    today = date.today()
    expiring_until = today + timedelta(days=expiring_within_days)

    quoted_ids = (
        session.query(Quotes.insurance_request_id)
        .filter(Quotes.insurance_company_id == company_id)
        .filter(_not_deleted(Quotes.deleted))
        .filter(Quotes.insurance_request_id.is_not(None))
    )
    unquoted_pending = (
        session.query(func.count(InsuranceRequests.id))
        .filter(_not_deleted(InsuranceRequests.deleted))
        .filter(InsuranceRequests.status == "pending")
        .filter(InsuranceRequests.id.notin_(quoted_ids))
    )
    for clause in _in_date_range(InsuranceRequests.created_at, from_date, to_date):
        unquoted_pending = unquoted_pending.filter(clause)
    unquoted_pending_requests = int(unquoted_pending.scalar() or 0)

    quotes_query = (
        session.query(
            func.count(Quotes.id),
            func.coalesce(func.sum(Quotes.premium), 0),
            func.avg(Quotes.premium),
        )
        .filter(Quotes.insurance_company_id == company_id)
        .filter(_not_deleted(Quotes.deleted))
    )
    for clause in _in_date_range(Quotes.created_at, from_date, to_date):
        quotes_query = quotes_query.filter(clause)
    quotes_total, quoted_premium_total, quoted_premium_average = quotes_query.one()
    quotes_total = int(quotes_total or 0)
    quotes_by_status = _counts_by(
        session, Quotes, Quotes.status, company_id, Quotes.created_at, from_date, to_date
    )

    policies_base = (
        session.query(Policies)
        .filter(Policies.insurance_company_id == company_id)
        .filter(_not_deleted(Policies.deleted))
    )
    for clause in _in_date_range(Policies.created_at, from_date, to_date):
        policies_base = policies_base.filter(clause)

    policies_total = int(policies_base.with_entities(func.count(Policies.id)).scalar() or 0)
    policies_expired = int(
        policies_base.with_entities(func.count(Policies.id))
        .filter((Policies.end_date < today) | (Policies.status == "expired"))
        .scalar()
        or 0
    )
    policies_active = int(
        policies_base.with_entities(func.count(Policies.id))
        .filter(Policies.status == "active")
        .filter(Policies.end_date >= today)
        .scalar()
        or 0
    )
    policies_expiring_soon = int(
        policies_base.with_entities(func.count(Policies.id))
        .filter(Policies.status == "active")
        .filter(Policies.end_date >= today)
        .filter(Policies.end_date <= expiring_until)
        .scalar()
        or 0
    )

    missing_docs_query = (
        session.query(func.count(Policies.id))
        .outerjoin(
            PolicyDocuments,
            and_(
                PolicyDocuments.policy_id == Policies.id,
                _not_deleted(PolicyDocuments.deleted),
            ),
        )
        .filter(Policies.insurance_company_id == company_id)
        .filter(_not_deleted(Policies.deleted))
        .filter(PolicyDocuments.id.is_(None))
    )
    for clause in _in_date_range(Policies.created_at, from_date, to_date):
        missing_docs_query = missing_docs_query.filter(clause)
    missing_documents = int(missing_docs_query.scalar() or 0)

    conversion_rate = round(policies_total / quotes_total, 4) if quotes_total else 0.0

    payments_query = (
        session.query(
            Payments.status,
            Payments.payment_method,
            func.count(Payments.id),
            func.coalesce(func.sum(Payments.amount), 0),
        )
        .filter(Payments.insurance_company_id == company_id)
        .filter(_not_deleted(Payments.deleted))
    )
    payment_date = func.coalesce(Payments.paid_at, Payments.created_at)
    for clause in _in_date_range(payment_date, from_date, to_date):
        payments_query = payments_query.filter(clause)
    payment_rows = payments_query.group_by(Payments.status, Payments.payment_method).all()

    status_buckets: dict[str, dict] = {}
    method_buckets: dict[str, dict] = {}
    collected_total = 0.0
    pending_total = 0.0
    for status, method, count, amount in payment_rows:
        amount_f = _money(amount)
        count_i = int(count or 0)
        status_key = status or "unknown"
        method_key = method or "unknown"
        status_buckets.setdefault(status_key, {"count": 0, "amount": 0.0})
        status_buckets[status_key]["count"] += count_i
        status_buckets[status_key]["amount"] = _money(
            status_buckets[status_key]["amount"] + amount_f
        )
        method_buckets.setdefault(method_key, {"count": 0, "amount": 0.0})
        method_buckets[method_key]["count"] += count_i
        method_buckets[method_key]["amount"] = _money(
            method_buckets[method_key]["amount"] + amount_f
        )
        if status_key == "completed":
            collected_total = _money(collected_total + amount_f)
        elif status_key == "pending":
            pending_total = _money(pending_total + amount_f)

    product_quote_rows = (
        session.query(
            InsuranceProducts.id,
            InsuranceProducts.name,
            func.count(Quotes.id),
            func.coalesce(func.sum(Quotes.premium), 0),
        )
        .select_from(Quotes)
        .join(InsuranceRequests, InsuranceRequests.id == Quotes.insurance_request_id)
        .outerjoin(
            InsuranceProducts,
            InsuranceProducts.id == InsuranceRequests.insurance_product_id,
        )
        .filter(Quotes.insurance_company_id == company_id)
        .filter(_not_deleted(Quotes.deleted))
    )
    for clause in _in_date_range(Quotes.created_at, from_date, to_date):
        product_quote_rows = product_quote_rows.filter(clause)
    product_quote_rows = product_quote_rows.group_by(
        InsuranceProducts.id, InsuranceProducts.name
    ).all()

    product_policy_rows = (
        session.query(
            InsuranceProducts.id,
            InsuranceProducts.name,
            func.count(Policies.id),
        )
        .select_from(Policies)
        .join(InsuranceRequests, InsuranceRequests.id == Policies.insurance_request_id)
        .outerjoin(
            InsuranceProducts,
            InsuranceProducts.id == InsuranceRequests.insurance_product_id,
        )
        .filter(Policies.insurance_company_id == company_id)
        .filter(_not_deleted(Policies.deleted))
    )
    for clause in _in_date_range(Policies.created_at, from_date, to_date):
        product_policy_rows = product_policy_rows.filter(clause)
    product_policy_rows = product_policy_rows.group_by(
        InsuranceProducts.id, InsuranceProducts.name
    ).all()

    product_revenue_rows = (
        session.query(
            InsuranceProducts.id,
            InsuranceProducts.name,
            func.coalesce(func.sum(Payments.amount), 0),
        )
        .select_from(Payments)
        .join(Quotes, Quotes.id == Payments.quote_id)
        .join(InsuranceRequests, InsuranceRequests.id == Quotes.insurance_request_id)
        .outerjoin(
            InsuranceProducts,
            InsuranceProducts.id == InsuranceRequests.insurance_product_id,
        )
        .filter(Payments.insurance_company_id == company_id)
        .filter(_not_deleted(Payments.deleted))
        .filter(Payments.status == "completed")
    )
    for clause in _in_date_range(func.coalesce(Payments.paid_at, Payments.created_at), from_date, to_date):
        product_revenue_rows = product_revenue_rows.filter(clause)
    product_revenue_rows = product_revenue_rows.group_by(
        InsuranceProducts.id, InsuranceProducts.name
    ).all()

    mix: dict[str, dict] = {}
    def mix_key(product_id, name):
        return str(product_id) if product_id else (name or "Unknown")

    for product_id, name, count, premium in product_quote_rows:
        key = mix_key(product_id, name)
        mix[key] = {
            "product_id": product_id,
            "product_name": name or "Unknown",
            "quotes": int(count or 0),
            "policies": 0,
            "quoted_premium": _money(premium),
            "collected_premium": 0.0,
        }
    for product_id, name, count in product_policy_rows:
        key = mix_key(product_id, name)
        mix.setdefault(
            key,
            {
                "product_id": product_id,
                "product_name": name or "Unknown",
                "quotes": 0,
                "policies": 0,
                "quoted_premium": 0.0,
                "collected_premium": 0.0,
            },
        )
        mix[key]["policies"] = int(count or 0)
    for product_id, name, amount in product_revenue_rows:
        key = mix_key(product_id, name)
        mix.setdefault(
            key,
            {
                "product_id": product_id,
                "product_name": name or "Unknown",
                "quotes": 0,
                "policies": 0,
                "quoted_premium": 0.0,
                "collected_premium": 0.0,
            },
        )
        mix[key]["collected_premium"] = _money(amount)

    month_start = from_date.replace(day=1) if from_date else date(today.year - 1, today.month, 1)
    month_end = to_date or today

    quote_months = (
        session.query(
            func.to_char(func.date_trunc("month", Quotes.created_at), "YYYY-MM"),
            func.count(Quotes.id),
        )
        .filter(Quotes.insurance_company_id == company_id)
        .filter(_not_deleted(Quotes.deleted))
        .filter(cast(Quotes.created_at, Date) >= month_start)
        .filter(cast(Quotes.created_at, Date) <= month_end)
        .group_by(func.date_trunc("month", Quotes.created_at))
        .all()
    )
    policy_months = (
        session.query(
            func.to_char(func.date_trunc("month", Policies.created_at), "YYYY-MM"),
            func.count(Policies.id),
        )
        .filter(Policies.insurance_company_id == company_id)
        .filter(_not_deleted(Policies.deleted))
        .filter(cast(Policies.created_at, Date) >= month_start)
        .filter(cast(Policies.created_at, Date) <= month_end)
        .group_by(func.date_trunc("month", Policies.created_at))
        .all()
    )
    revenue_months = (
        session.query(
            func.to_char(
                func.date_trunc("month", func.coalesce(Payments.paid_at, Payments.created_at)),
                "YYYY-MM",
            ),
            func.coalesce(func.sum(Payments.amount), 0),
        )
        .filter(Payments.insurance_company_id == company_id)
        .filter(_not_deleted(Payments.deleted))
        .filter(Payments.status == "completed")
        .filter(cast(func.coalesce(Payments.paid_at, Payments.created_at), Date) >= month_start)
        .filter(cast(func.coalesce(Payments.paid_at, Payments.created_at), Date) <= month_end)
        .group_by(func.date_trunc("month", func.coalesce(Payments.paid_at, Payments.created_at)))
        .all()
    )

    monthly_map: dict[str, dict] = {}
    cursor = date(month_start.year, month_start.month, 1)
    end_month = date(month_end.year, month_end.month, 1)
    while cursor <= end_month:
        key = cursor.strftime("%Y-%m")
        monthly_map[key] = {"month": key, "quotes": 0, "policies": 0, "revenue": 0.0}
        if cursor.month == 12:
            cursor = date(cursor.year + 1, 1, 1)
        else:
            cursor = date(cursor.year, cursor.month + 1, 1)
    for month, count in quote_months:
        if month in monthly_map:
            monthly_map[month]["quotes"] = int(count or 0)
    for month, count in policy_months:
        if month in monthly_map:
            monthly_map[month]["policies"] = int(count or 0)
    for month, amount in revenue_months:
        if month in monthly_map:
            monthly_map[month]["revenue"] = _money(amount)

    report = {
        "company_id": company.id,
        "company_name": company.name,
        "period": {"from_date": from_date, "to_date": to_date},
        "pipeline": {
            "unquoted_pending_requests": unquoted_pending_requests,
            "quotes_total": quotes_total,
            "quotes_by_status": [
                {"status": status, "count": count}
                for status, count in sorted(quotes_by_status.items())
            ],
            "quoted_premium_total": _money(quoted_premium_total),
            "quoted_premium_average": _money(quoted_premium_average),
            "conversion_rate": conversion_rate,
        },
        "policies": {
            "total": policies_total,
            "active": policies_active,
            "expired": policies_expired,
            "expiring_soon": policies_expiring_soon,
            "missing_documents": missing_documents,
        },
        "revenue": {
            "collected_total": collected_total,
            "pending_total": pending_total,
            "payments_by_status": [
                {"key": key, "count": val["count"], "amount": val["amount"]}
                for key, val in sorted(status_buckets.items())
            ],
            "payments_by_method": [
                {"key": key, "count": val["count"], "amount": val["amount"]}
                for key, val in sorted(method_buckets.items())
            ],
        },
        "product_mix": sorted(mix.values(), key=lambda item: item["product_name"]),
        "monthly": list(monthly_map.values()),
    }
    logger.info(f"Analytics report generated for company {company_id}")
    return report
