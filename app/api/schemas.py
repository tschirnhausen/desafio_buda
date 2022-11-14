from pydantic import BaseModel
from pydantic.types import PositiveFloat
from api.constants import AlertType


class Alert(BaseModel):
    """
    Serializer for Alert model.
    See api/models -> Alert
    """
    type: AlertType
    currency: str
    market: str
    spread: PositiveFloat

    class Config:
        orm_mode = True
