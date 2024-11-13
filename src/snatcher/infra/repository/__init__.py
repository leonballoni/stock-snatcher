from abc import ABC, abstractmethod
from typing import List
from infra.schema import GetStockOutput, StockSchema
from datetime import date


class AbsStockRepository(ABC):

    @abstractmethod
    def get(self, stock_id: int) -> GetStockOutput:
        raise NotImplementedError

    @abstractmethod
    def post_purchase_order(self, stock_id: int, amount: int):
        raise NotImplementedError

    @abstractmethod
    def save(self, stock: StockSchema):
        raise NotImplementedError

    @abstractmethod
    def remove(self, stock_id: int):
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[GetStockOutput]:
        raise NotImplementedError


class AbsPoligyonRepository(ABC):

    @abstractmethod
    def get_daily_open_close(self, stock_symbol: str, specific_date: date):
        raise NotImplementedError


class AbsMarketWatchRepository(ABC):

    @abstractmethod
    def get_competitors(self):
        raise NotImplementedError

    @abstractmethod
    def get_performance(self):
        raise NotImplementedError

    @abstractmethod
    def get_stock_list(self):
        pass
