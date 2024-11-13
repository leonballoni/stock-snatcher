from enum import Enum


class Messages(Enum):
    DATABASE_ERROR = "Database error"
    STOCK_NOT_FOUND = "Search for another Stock code"
    BAD_PURCHASE_AMOUNT = "Check if the value is negative or zero"
    POLYGON_REQUEST_FAILURE = "Check if the params, headers or anything else is valid/correct with polygon API documentation"
    PYDANTIC_VALIDATION_ERROR = "Check if the given attributes are valid"
    FIELD_NAME_VALUE_ERROR = "Check if field name or field value is correct"
    ATTRIBUTE_ERROR = "Error at field retrieving/usage"
