from schemas.admin_schema import *
from schemas.agent_schema import *
from schemas.insuranceProduct_schema import *
from schemas.requests_schema import *
from typing import List, Optional
from pydantic import ConfigDict, Field


class quoteCreateInterface(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    #insurance_company_id: str = Field(alias="insuranceCompanyId")
    premium: float
    agent_commission: float = Field(alias="agentCommission")
    status: str
    info: str
    insurance_request_id: str = Field(alias="insuranceRequestId")


class QuoteBatchCreate(BaseModel):
    items: List[quoteCreateInterface]
    
class quoteInterface(BaseModel):
    id: str
    insurance_company_id: str = Field(alias="insuranceCompanyId")
    premium: float
    agent_commission: float = Field(alias="agentCommission")
    status: str
    info: str
    insurance_request_id: str = Field(alias="insuranceRequestId")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

class quoteModelInterface(BaseModel):
    id: str
    insurance_company_id: str = Field(alias="insuranceCompanyId")
    premium: float
    agent_commission: float = Field(alias="agentCommission")
    status: str
    info: str
    insurance_request_id: str = Field(alias="insuranceRequestId")
    agent: agentModelInterface

    insurance_company: adminModelInterface = Field(alias="insuranceCompany")
    deleted: bool
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    created_by: str = Field(alias="createdBy")
    agency_rate: float = Field(alias="agencyRate")
    agent_rate: float = Field(alias="agentRate")
    system_commission: float = Field(alias="systemCommission")


class quoteUpdateInterface(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    insurance_company_id: Optional[str] = Field(alias="insuranceCompanyId", default=None)
    premium: Optional[float] = None
    agent_commission: Optional[float] = Field(alias="agentCommission", default=None)
    status: Optional[str] = None
    insurance_request_id: Optional[str] = Field(alias="insuranceRequestId", default=None)

class quoteRequestUpdateInterface(BaseModel):
    status: Optional[str] = None
    reason: Optional[str] = None
    responded_by: Optional[str] = Field(alias="respondedBy", default=None)

class quotePremiumUpdateInterface(BaseModel):
    premium: Optional[float] = None
    info: Optional[str] = None
