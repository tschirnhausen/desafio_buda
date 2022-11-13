from enum import Enum


class AlertType(str, Enum):
    """
    Types of alerts for an Alert Model
    See api/models -> Alert
    """
    under = 'under'
    above = 'above'


class AlertStatus(str, Enum):
    """
    An spread can be under or above a threshold, if the condition is met, alert status changes to fullfil,
    in any other case is pending.

    Undefined status is not used yet.
    """
    fulfill = 'fulfill'
    pending = 'pending'
    undefined = 'undefined'