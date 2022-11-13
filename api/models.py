from database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy_utils.types.choice import ChoiceType
from api.constants import AlertType


class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(ChoiceType(AlertType, impl=String()))
    market = Column(String)
    spread = Column(Float)
