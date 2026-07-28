# schemas/insurance_types_schemas.py
from uuid import UUID
from pydantic import BaseModel

class InsuranceTypeOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True  # or orm_mode = True depending on your Pydantic version