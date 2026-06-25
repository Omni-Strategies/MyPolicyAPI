from typing import TypedDict
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
    country_id: str
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: str
    roles: list[str]
    image: ImageDict



class customerAgentCreateUserInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    customer_type: str
    gh_card_no: str
    image: ImageDict


class customerUpdateUserInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    dob: str
    country_id: str
    customer_type: str
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: str
    roles: list[str]
    password: str
    image: ImageDict | str


class customerUserInterface(BaseModel):
    id: str
    first_name: str
    last_name: str
    country_id: str
    customer_type: str
    gender: str
    gh_card_no: str
    digital_address: str
    business_entity_id: str
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