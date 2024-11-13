from fastapi import Depends, Response
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from app.stock import StockService
from infra.exception import (
    PurchaseAmountInvalid,
    StockSymbolNotFound,
    DatabaseError,
    FieldNameNotFound,
)
from infra.model.database import DatabaseSession
from infra.repository.stock import StockRepository
from infra.schema import (
    GetStockOutput,
    GetStockInput,
    StockBuyOrderOutput,
    StockBuyOrderInput,
)
from settings import Config
from pydantic import Field
from typing import Annotated
from infra.exception.http import ErrorHandler
from infra.controller.generic import GenericApi


class StockController(GenericApi):

    def __init__(self, config: Config, *args, **kwargs):
        tags = ["stocks"]
        prefix = "/stock"
        self.cfg = config
        super().__init__(tags=tags, prefix=prefix, *args, **kwargs)

        self.add_api_route(
            path="/{stock_symbol}",
            endpoint=self.get_stock,
            methods=["GET"],
            response_model=GetStockOutput,
            responses={
                404: {"description": "Stock not found."},
                500: {
                    "description": (
                        "Internal Server Error. Possible reasons include:\n",
                        "2. Database Failure",
                    )
                },
            },
        )
        self.add_api_route(
            path="/{stock_symbol}",
            endpoint=self.post_purchase_stock,
            methods=["POST"],
            status_code=201,
            response_model=StockBuyOrderOutput,
            responses={
                404: {"description": "Stock not found."},
                422: {
                    "description": (
                        "Unprocessable Entity. Possible reasons include:\n"
                        "1. Validation error.\n"
                        "2. Amount less than or equal to 0.\n"
                    )
                },
                500: {"description": "Internal Server Error"},
            },
        )

    async def get_stock(
        self,
        request: Request,
        input_param: Annotated[
            GetStockInput, Depends(), Field(description="Stock to check")
        ],
        session: Session = Depends(DatabaseSession()),
    ):
        """
        Retrieves the StockModel with general information.

        - **stock_symbol (str)**: stock to buy

        **Returns**:
        - A JSON object with Stock Model Entity
        - HTTP 404 if the stock symbol was not found.
        - HTTP 500 if there is an internal server error.

        """
        try:
            service = StockService(self.cfg, StockRepository(session))
            response = await service.get_stock(stock_input=input_param)
            return response
        except FieldNameNotFound as exp:
            ErrorHandler.handle_field_name_not_found(exp)
        except StockSymbolNotFound as exp:
            ErrorHandler.handle_stock_not_found(exp)
        except Exception as exp:
            raise exp

    @staticmethod
    async def post_purchase_stock(
        request: Request,
        stock_symbol: Annotated[str, Field(description="Stock/Ação a ser comprada")],
        order: Annotated[StockBuyOrderInput, Field(description="Ordem de compra")],
        session: Session = Depends(DatabaseSession()),
    ):
        """
        Create a new buy order

        - **stock_symbol (str)**: Stock to buy
        - **amount (StockBuyOrderInput)**: Amount to buy

        **Returns**:
        -  A JSON object with the stock symbol and amount if successful.
        - HTTP 404 if the stock symbol was not found.
        - HTTP 422 if the amount is less than or equal to zero or there is a validation error.
        - HTTP 500 if there is an internal server error.
        """
        try:
            service = StockService(StockRepository(session))
            purchased_amount = await service.post_purchase_stock(
                stock_symbol, order.amount
            )
            success_message = f"{purchased_amount} units of stock {stock_symbol} were added to your stock record"
            content = StockBuyOrderOutput(message=success_message).model_dump_json(
                indent=4
            )
            return Response(
                content=content,
                status_code=201,
                media_type="application/json",
            )
        except AttributeError as exp:
            ErrorHandler.handle_attribute_error(exp)
        except StockSymbolNotFound as exp:
            ErrorHandler.handle_stock_not_found(exp)
        except PurchaseAmountInvalid as exp:
            ErrorHandler.handle_purchase_amount_invalid(exp)
        except DatabaseError as exp:
            ErrorHandler.handle_database_error(exp)
        except Exception as exp:
            raise HTTPException(
                status_code=500, detail=f"Erro inesperado: {exp}"
            ) from exp
