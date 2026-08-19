from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StatusCount(BaseModel):
    status: str
    count: int


class AmountBucket(BaseModel):
    key: str
    count: int
    amount: float


class ProductMixItem(BaseModel):
    product_id: Optional[UUID] = None
    product_name: str
    quotes: int
    policies: int
    quoted_premium: float
    collected_premium: float


class MonthlyPoint(BaseModel):
    month: str
    quotes: int
    policies: int
    revenue: float


class AnalyticsPeriod(BaseModel):
    from_date: Optional[date] = None
    to_date: Optional[date] = None


class PipelineAnalytics(BaseModel):
    unquoted_pending_requests: int
    quotes_total: int
    quotes_by_status: list[StatusCount]
    quoted_premium_total: float
    quoted_premium_average: float
    conversion_rate: float = Field(description="Policies issued / quotes submitted")


class PolicyAnalytics(BaseModel):
    total: int
    active: int
    expired: int
    expiring_soon: int
    missing_documents: int


class RevenueAnalytics(BaseModel):
    collected_total: float
    pending_total: float
    payments_by_status: list[AmountBucket]
    payments_by_method: list[AmountBucket]


class CompanyAnalyticsReport(BaseModel):
    company_id: UUID
    company_name: str
    period: AnalyticsPeriod
    pipeline: PipelineAnalytics
    policies: PolicyAnalytics
    revenue: RevenueAnalytics
    product_mix: list[ProductMixItem]
    monthly: list[MonthlyPoint]
