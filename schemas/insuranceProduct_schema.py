from pydantic import BaseModel

class insuranceProductModelInterface(BaseModel):
    id: str
    name: str
    image: str
    createdAt: str
    updatedAt: str