from .admin_schema import adminModelInterface
from .insuranceProduct_schema import insuranceProductModelInterface
from .insurance_company_schema import InsuranceCompanyModel
from pydantic import BaseModel

class insuranceCommissionCreateInterface(BaseModel):
    insurance_company_id: str
    agent_rate: float
    agency_rate: float
    cover_type: str
    insurance_product_id: str



class insuranceCommissionModelInterface(BaseModel):
    id: str
    insurance_company_id: str
    agent_rate: float
    agency_rate: float
    cover_type: str
    insurance_product_id: str
    admin: adminModelInterface
    deleted: bool
    created_at: str
    updated_at: str

from typing import Optional

class InsuranceCommissionModel:
    id: str
    insurance_company_id: str
    agent_rate: float
    agency_rate: float
    cover_type: str
    insurance_product_id: str
    admin: adminModelInterface
    deleted: bool
    created_at: str
    updated_at: str
    insurance_product: Optional[insuranceProductModelInterface] = None
    insurance_company: Optional[InsuranceCompanyModel] = None

class InsuranceCommissionUpdateInterface(BaseModel):
    insurance_company_id: str
    insurance_product_id: str
    cover_type: str
    agent_rate: float
    agency_rate: float