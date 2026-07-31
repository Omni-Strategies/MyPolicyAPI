from pydantic import BaseModel
from typing import Union, Optional



class LogoData(BaseModel):
    fileName: str
    base64: str


class InsuranceCompanyCreate(BaseModel):
    name: str
    logo: Optional[Union[LogoData, str]]
    emails: list[str]
    phone_numbers: list[str]
    digital_address: str
    address_line_1: str
    country: str
    address_line_2: Optional[str]


class InsuranceCompany(BaseModel):
    id: str
    name: str
    logo: str
    createdAt: str
    updatedAt: str


class InsuranceCompanyModel(BaseModel):
    id: str
    name: str
    logo: str
    created_at: str
    updated_at: str


class InsuranceCompanyUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[Union[LogoData, str]] = None
