from pydantic import BaseModel
from typing import Union



class LogoData(BaseModel):
    fileName: str
    base64: str


class InsuranceCompanyCreate(BaseModel):
    name: str
    logo: Union[LogoData, str]


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
    name: str
    logo: str
