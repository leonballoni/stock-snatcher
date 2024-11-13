from infra.model import StockModel
from infra.schema import (
    GetStockOutput,
    StockValuesSchema,
    PerformanceDataSchema,
    CompetitorSchema,
)
from typing import Type, List
import asyncio


class CompetitorAggregate:
    def __init__(self):
        pass

    async def get_competitor(self):
        pass

    async def add_competitor(self):
        pass


class StockValuesAggregate:
    def __init__(self):
        pass

    async def get_stock_value(self):
        pass

    async def add_stock_value(self):
        pass


class StockAggregate:
    def __init__(self, stock_model: StockModel):
        self.stock_model = stock_model

    async def add_purchase_order(self) -> GetStockOutput:
        return await self.validated_stock_model(self.stock_model)

    async def get_stock(self) -> GetStockOutput:
        return await self.validated_stock_model(self.stock_model)

    @staticmethod
    async def validated_stock_model(stock_model: StockModel) -> GetStockOutput:
        async def extract_stock_values(model: Type[StockModel]) -> StockValuesSchema:
            return StockValuesSchema(
                open=model.stock_values.open,
                high=model.stock_values.high,
                low=model.stock_values.low,
                close=model.stock_values.close,
            )

        async def extract_performance_data(
            model: Type[StockModel],
        ) -> PerformanceDataSchema:
            return PerformanceDataSchema(
                five_days=model.performance_data.five_days,
                one_month=model.performance_data.one_month,
                three_months=model.performance_data.three_months,
                year_to_date=model.performance_data.year_to_date,
                one_year=model.performance_data.one_year,
            )

        async def extract_competitors(
            model: Type[StockModel],
        ) -> List[CompetitorSchema]:
            return [
                CompetitorSchema.model_validate(
                    **{
                        "company_name": competitor.company_name,
                        "market_cap": {
                            "currency": competitor.currency,
                            "value": competitor.value,
                        },
                    }
                )
                for competitor in model.competitors
            ]

        stock_values, performance_data, competitors = await asyncio.gather(
            extract_stock_values(stock_model),
            extract_performance_data(stock_model),
            extract_competitors(stock_model),
        )

        return GetStockOutput(
            status=stock_model.status,
            purchased_amount=stock_model.purchased_amount,
            purchased_status=stock_model.purchased_status,
            request_date=stock_model.request_date,
            company_code=stock_model.stock_company.code,
            company_name=stock_model.stock_company.name,
            stock_values=stock_values,
            performance_data=performance_data,
            competitors=competitors,
        )
