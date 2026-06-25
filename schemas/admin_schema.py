from pydantic import BaseModel
from schemas.role_schema import *

class ImageDict(BaseModel):
    file_name: str
    base64: str

class adminCreateUserInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str
    phone: str
    roles: list[str]
    password: str
    image: ImageDict

class adminUpdateUserInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str
    phone: str
    roles: list[str]
    password: str
    image: ImageDict


class adminUserInterface(BaseModel):
    id: str
    first_name: str
    last_name: str
    password: str
    email: str
    department: str
    createdAt: str

class adminModelInterface(BaseModel):
    id: str
    first_name: str
    last_name: str
    password: str
    email: str
    department: str
    image: str
    phone: str
    roles: list[str]
    status: str
    createdAt: str
    roles_list: list[roleModelInterface]

class adminUpdateStatusInterface(BaseModel):
    status: str