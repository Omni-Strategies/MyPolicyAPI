from pydantic import BaseModel

class roleCreateInterface(BaseModel):
    name: str
    organizationId: str
    roleType: str

class roleInterface(BaseModel):
    id: str
    name: str
    role_type: str
    organization_id: str
    deleted: bool
    createdAt: str
    updatedAt: str

class roleModelInterface(BaseModel):
    id: str
    name: str
    role_type: str
    organization_id: str
    deleted: bool
    created_at: str
    updated_at: str

class roleUpdateInterface(BaseModel):
    name: str
 