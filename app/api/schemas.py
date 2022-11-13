from pydantic import BaseModel
from api.constants import AlertType

class Alert(BaseModel):
    """
    Serializer for Alert model.
    See api/models -> Alert
    """
    type: AlertType
    currency: str
    market: str
    spread: float

    class Config:
        orm_mode = True
