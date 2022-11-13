from pydantic import BaseModel
from api.constants import AlertType

class Alert(BaseModel):
    type: AlertType
    market: str
    spread: float

    class Config:
        orm_mode = True
