from pydantic import BaseModel


class insuranceBrokerModelInterface(BaseModel):
    id: str
    name: str
    logo: str
    createdAt: str
    updatedAt: str