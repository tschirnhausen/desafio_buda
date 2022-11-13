from database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy_utils.types.choice import ChoiceType
from api.constants import AlertType


class Alert(Base):
    """
    Alert main model used for check if a market price is above or under a threshold
    """
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(ChoiceType(AlertType, impl=String()))
    currency = Column(String)
    market = Column(String)
    spread = Column(Float)
