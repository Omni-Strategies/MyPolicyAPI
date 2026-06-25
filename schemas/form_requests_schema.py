from pydantic import BaseModel
from typing import TypedDict, Any
from schemas.customer_schema import *
from schemas.admin_schema import *
from schemas.insuranceProduct_schema import insuranceProductModelInterface

class Image(BaseModel):
    file_name: str
    base64: str

class FormRequestCreateInterface(BaseModel):
    insurance_product_id: str
    request_data: Any
    vehicle_image: Image
    vehicle_image2: Image
    road_doc1: Image
    road_doc2: Image
    
class FormRequestInterface(BaseModel):
    insurance_product_id: str
    request_data: Any
    vehicle_image: str
    vehicle_image2: str
    road_doc1: str
    road_doc2: str
    status: str
    reason: str|None
    deleted: bool
    created_at: str
    updated_at: str

class FormRequestModelInterface:
    id: str
    insurance_product_id: str
    request_data: Any
    vehicle_image: str
    vehicle_image2: str
    road_doc1: str
    road_doc2: str
    status: str
    reason: str|None
    deleted: bool
    created_at: str
    updated_at: str
    requested_by: str|None
    responded_by: str|None
    customer: customerModelInterface
    admin: adminModelInterface
    insurance_product: insuranceProductModelInterface

class FormRequestUpdateInterface(BaseModel):
    status: str
    reason: str|None

class FormRequestDataUpdateInterface(BaseModel):
    insurance_product_id: str
    request_data: Any
    assigned_agent_id: str
    assigned_agent_id: str
    requested_by: str
