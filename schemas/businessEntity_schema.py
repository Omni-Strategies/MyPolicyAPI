from typing import TypedDict
from pydantic import BaseModel



class ImageDict(BaseModel):
    file_name: str
    base64: str


class CustomerRegisterInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    dob: str
    countryId: str
    gender: str
    ghCardNo: str
    digital_address: str
    buisnessEntityId: str
    roles: list[str]
    image: ImageDict

class logo(BaseModel):
    file_name: str
    base64: str

class businessEntityRegisterInterface(BaseModel):
    name: str
    tinNo: str
    logo: logo|str
    customer: CustomerRegisterInterface

class businessEntityCreateInterface(BaseModel):
    name: str
    tinNo: str
    logo: logo|str
    
class businessEntityInterface(BaseModel):
    id: str
    name: str
    logo: str
    createdAt: str
    updated: str

class businessEntityModelInterface(BaseModel):
    id: str
    name: str
    tin_no: str
    logo: str
    created_at: str
    updated_at: str

class businessEntityUpdateInterface(BaseModel):
    name: str
    logo: str