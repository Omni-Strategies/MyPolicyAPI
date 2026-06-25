from typing import Optional, Any
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from schemas.agent_schema import *
from schemas.admin_schema import *

from schemas.customer_schema import customerModelInterface
from schemas.insuranceProduct_schema import *

class InsuranceRequestCreateInterface(BaseModel):
    insurance_product_id: str
    request_data: dict
    requested_by: Optional[str]
    intermediary_id: str
    assigned_agency_id: str
    assigned_agent_id: str

class insuranceRequestInterface(BaseModel):
    id: str
    insurance_product_id: str
    requestData: Any
    registeredNo: str
    status: str
    reason: Optional[str]
    deleted: bool
    requestedBy: Optional[str]
    intermediaryId: str
    createdAt: str
    updatedAt: str

class insuranceRequestModelInterface:
    id: str
    insurance_product_id: str
    registered_no: str
    request_data: Any
    quotes_count: Any
    reason: Optional[str]
    intermediary_id: Optional[str]
    assigned_agent_id: Optional[str]
    assigned_agency_id: Optional[str]
    status: str
    deleted: bool
    created_at: str
    updated_at: str
    customer: customerModelInterface
    agent: agentModelInterface
    admin: adminModelInterface
    insurance_product: insuranceProductModelInterface


class  InsuranceRequestUpdateInterface(BaseModel):
    status: str
    reason: Optional[str]

class insuranceRequestDataUpdateInterface(BaseModel):
    request_data: Any
