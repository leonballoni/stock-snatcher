from infra.enumerator.http_exception import Messages
from infra.exception import (
    DatabaseError,
    StockSymbolNotFound,
    PurchaseAmountInvalid,
    PolygonRequestFailure,
    PydanticValidationError,
    FieldNameNotFound,
)
from fastapi import HTTPException, status
from loguru import logger
from httpx import RequestError


class ErrorHandler:
    """
    Class responsable for centralizing the project exceptions
    """

    @staticmethod
    def handle_database_error(exc: DatabaseError) -> None:
        """
        Returns error 500 due to Database Failure
        """
        logger.error(f"Error in Database: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Messages.DATABASE_ERROR.value,
        )

    @staticmethod
    def handle_stock_not_found(exp: StockSymbolNotFound) -> None:
        """
        HTTP 404 if the stock symbol was not found.
        """
        logger.error(f"Stock not found error: {exp.message}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=Messages.STOCK_NOT_FOUND.value
        )

    @staticmethod
    def handle_purchase_amount_invalid(exp: PurchaseAmountInvalid) -> None:
        """
        HTTP 422 amount incorrect
        """
        logger.error(f"Purchase amount is invalid: {exp.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Messages.BAD_PURCHASE_AMOUNT.value,
        )

    @staticmethod
    def handle_polygon_api_failed_request(
        status_code: int, exp: PolygonRequestFailure | RequestError
    ) -> None:
        """
        HTTP 500/400 for api request failure
        """
        logger.error(f"Polygon request failed: {exp}")
        raise HTTPException(
            status_code=status_code,
            detail=Messages.POLYGON_REQUEST_FAILURE.value,
        )

    @staticmethod
    def handle_pydantic_validation_error(exp: PydanticValidationError) -> None:
        """
        HTTP 422 or 400 for used attributes
        """
        logger.error(f"Pydantic validation failed: {exp}")
        raise HTTPException(
            status_code=400,
            detail=Messages.PYDANTIC_VALIDATION_ERROR.value,
        )

    @staticmethod
    def handle_field_name_not_found(exp: FieldNameNotFound) -> None:
        """
        HTTP 422 or 400 for used attributes
        """
        logger.error(f"Failed to find field name or value: {exp}")
        raise HTTPException(
            status_code=404,
            detail=Messages.FIELD_NAME_VALUE_ERROR.value,
        )

    @staticmethod
    def handle_attribute_error(exp: AttributeError) -> None:
        """
        HTTP 422 or 400 for used attributes
        """
        logger.error(f"Error at getattr method: {exp}")
        raise HTTPException(
            status_code=400,
            detail=Messages.ATTRIBUTE_ERROR.value,
        )
