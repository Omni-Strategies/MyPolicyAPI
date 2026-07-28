from typing import TypedDict, Optional
from pydantic import BaseModel
from schemas.businessEntity_schema import *
from schemas.role_schema import *


class ImageDict(BaseModel):
    file_name: str
    base64: str


class CustomerRegisterInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str
    dob: str
    country_id: Optional[str] = None
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: Optional[str] = None
    roles: list[str]
    image: Optional[ImageDict] = None



class customerAgentCreateUserInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    customer_type: str
    gh_card_no: str
    image: Optional[ImageDict] = None


class customerUpdateUserInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    dob: str
    country_id: Optional[str] = None
    customer_type: str
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: Optional[str] = None
    roles: list[str]
    password: str
    image: Optional[ImageDict] = None


class customerUserInterface(BaseModel):
    id: str
    first_name: str
    last_name: str
    country_id: Optional[str] = None
    customer_type: str
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: Optional[str] = None
    password: str
    email: str
    created_at: str


class customerModelInterface(BaseModel):
    id: str
    first_name: str
    last_name: str
    password: str
    country_id: str
    customer_type: str
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: str
    email: str
    image: str
    phone: str
    dob: str
    roles: list[str]
    business_entity: businessEntityModelInterface
    created_at: str
    roles_list: list[roleModelInterface]