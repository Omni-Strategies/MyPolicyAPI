from pydantic import BaseModel
from schemas.role_schema import *
from schemas.insuranceBroker_schema import *

class agentModelInterface(BaseModel):
    id: str
    first_name: str
    last_name: str
    password: str
    country_id: str
    physical_address: str
    postal_address: str
    digital_address: str
    intermidary_type: str
    agent_code: str
    email: str
    image: str
    status: str
    nic_document: str
    agreement_document: str
    phone: str
    roles: list[str]
    organization_id: str
    organization: insuranceBrokerModelInterface
    created_at: str
    roles_list: list[roleModelInterface]
