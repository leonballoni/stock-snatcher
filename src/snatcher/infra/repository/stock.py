from datetime import datetime, date

from infra.exception import StockSymbolNotFound, FieldNameNotFound
from infra.repository import AbsStockRepository
from sqlalchemy.orm import Session
from sqlalchemy import and_
from loguru import logger
from infra.model.stock import StockModel, StockCompany, Base
from typing import Type, TypeVar, List, Dict, Union
from infra.model.database import DatabaseSession
from infra.schema import GetStockOutput, StockSchema

T = TypeVar("T", bound=Base)


class StockRepository(AbsStockRepository):
    def save(self, stock: StockSchema):
        pass

    def remove(self, stock_id: int):
        pass

    def find_all(self) -> List[GetStockOutput]:
        pass

    def __init__(self, session: Session):
        self.session = session
        self.db_actions = DatabaseSession()

    async def get_by_field(
        self, model: Type[T], fields: List[Dict[str, Union[str | int | date]]]
    ) -> T:
        """
        Args:
            model (): The SQLAlchemy model class to query.
            fields (): A list of dictionaries specifying field name and value pairs to filter the query by.

        Returns:
            The queried model instance matching the specified fields, or None if no match is found.

        Raises:
            FieldNameNotFound: If no result is found matching the specified fields.
            AttributeError: If there is an error setting up the filters with the specified fields.
        """
        try:
            filters = [
                getattr(model, field_name) == field_value
                for field in fields
                for field_name, field_value in field.items()
            ]
            result = self.session.query(model).filter(and_(*filters)).one_or_none()
            if not result:
                error_msg = f"failure to setup filter: {fields}"
                logger.error(error_msg)
                raise FieldNameNotFound(error_msg)
            return result
        except AttributeError as exp:
            raise AttributeError(f"Failed to setup filter: {fields}") from exp

    async def get(self, stock_id: int) -> StockModel:
        """
        Args:
            stock_id (int): The unique identifier for the stock item.

        Returns:
            StockModel: An asynchronous operation that returns the StockModel object corresponding to the given stock identifier.
        """
        return await self.get_by_field(StockModel, [{"id": stock_id}])

    async def get_by_stock_symbol(self, stock_symbol: str) -> StockModel:
        """
        Args:
            stock_symbol (str): The stock symbol used to identify the stock company.

        Returns:
            StockModel: The stock model that matches the given stock symbol.

        Raises:
            ValueError: If the stock symbol is not valid or cannot be found.
        """
        company = await self.check_stock_symbol(stock_symbol)
        return await self.get_by_field(StockModel, [{"stock_company_id": company.id}])

    async def post_purchase_order(self, stock_symbol: str, amount: int) -> StockModel:
        company = await self.get_by_field(StockCompany, [{"code": stock_symbol}])
        actual_model = await self.get_by_field(
            StockModel, [{"id": company.code, "request_date": datetime.now().date()}]
        )
        new_amount = actual_model.purchased_amount + amount
        actual_model.purchased_amount = new_amount
        actual_model = self.db_actions.create_session(self.session, actual_model)
        return actual_model

    async def check_stock_symbol(self, stock_symbol: str) -> Type[StockCompany]:
        company = (
            self.session.query(StockCompany)
            .filter(StockCompany.code == stock_symbol)
            .one_or_none()
        )
        if not company:
            error_msg = f"company of {stock_symbol} was not found"
            logger.error(error_msg)
            raise StockSymbolNotFound(error_msg)
        return company
