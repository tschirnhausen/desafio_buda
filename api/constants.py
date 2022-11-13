from enum import Enum


class AlertType(str, Enum):
    under = 'under'
    above = 'above'
