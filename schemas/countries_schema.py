from typing import TypedDict, Optional
from pydantic import BaseModel
from schemas.businessEntity_schema import *
from schemas.role_schema import *


class countryCreateInterface(BaseModel):
   name: str
    

class countryCreateInterface(BaseModel):
   id: str
   name: str
   created_at: str
   updated_at: str

class countryUpdateInterface(BaseModel):
   name: str