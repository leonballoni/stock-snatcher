from seedwork.exceptions.base import CustomException
from httpx import RequestError


class SettingsException(CustomException):
    pass


class PurchaseAmountInvalid(CustomException):
    pass


class StockSymbolNotFound(CustomException):
    pass


class FieldNameNotFound(CustomException):
    pass


class StockEntityNotFound(CustomException):
    pass


class DatabaseError(CustomException):
    pass


class PolygonRequestFailure(RequestError):
    pass


class PydanticValidationError(CustomException):
    pass
