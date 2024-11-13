from infra.exception import PurchaseAmountInvalid
from seedwork.exceptions.base import StandardErrorMessage
from seedwork.infra.schemas import PydanticModel
from pydantic import HttpUrl, field_validator
from typing import List
from fastapi import Header
from pydantic import Field
from datetime import date


class MarketCapSchema(PydanticModel):
    currency: str = Field(..., alias="Currency")
    value: float = Field(..., alias="Value")


class CompetitorSchema(PydanticModel):
    company_name: str
    market_cap: MarketCapSchema


class StockValuesSchema(PydanticModel):
    open: float
    high: float
    low: float
    close: float


class PerformanceDataSchema(PydanticModel):
    five_days: float
    one_month: float
    three_months: float
    year_to_date: float
    one_year: float


class StockCompany(PydanticModel):
    code: str
    name: str
    url: HttpUrl
    sector: str


class StockSchema(PydanticModel):
    status: str = Field(description="The status of this request's response.")
    purchased_amount: int
    purchased_status: str
    request_date: date
    stock_company: StockCompany
    stock_values: StockValuesSchema
    performance_data: PerformanceDataSchema
    competitors: List[CompetitorSchema]


class GetStockOutput(PydanticModel):
    status: str
    purchased_amount: int
    purchased_status: str
    request_date: date
    company_code: str
    company_name: str
    stock_values: StockValuesSchema
    performance_data: PerformanceDataSchema
    competitors: List[CompetitorSchema]


class GetStockInput(PydanticModel):
    stock_symbol: str


class StockBuyOrderInput(PydanticModel):
    amount: int = Field(..., gt=0)

    @field_validator("amount", mode="before")
    @classmethod
    def check_amount(cls, value: float):
        if value <= 0:
            error_msg = StandardErrorMessage.format_string_error_message(
                "Invalid stock amount"
            )
            raise PurchaseAmountInvalid(error_msg)
        new_value = round(value)
        return new_value


class StockBuyOrderOutput(PydanticModel):
    message: str = Field(
        default="{amount} units of stock {stock_symbol} were added to your stock record"
    )


class PostStockExtractorInput(PydanticModel):
    Authorization: str = Header(...)


class PostStockExtractorOutput(PydanticModel):
    message: str = Field(
        default="Stock data was extracted from the MarketWatch website and Polygon API"
    )
    detail: dict = Field(default={}, description="TBD")
