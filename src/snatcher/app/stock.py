from domain.aggregates import StockAggregate
from infra.repository.stock import StockRepository
from infra.schema import GetStockInput, GetStockOutput
from modules.redis import RedisServer
from settings import Config


class StockService:
    def __init__(self, config: Config, repository: StockRepository):
        self.repository = repository
        self.cfg = config
        self.redis = RedisServer(url=self.cfg.REDIS_URL)

    async def get_stock(self, stock_input: GetStockInput) -> GetStockOutput:
        """
        Args:
            stock_input (GetStockInput): The input containing the stock symbol for which stock details are to be fetched.

        Returns:
            GetStockOutput: The output containing the validated stock details.
        """
        cached_stock = self.redis.get_item(stock_input.stock_symbol)
        if cached_stock:
            return GetStockOutput.model_validate_json(cached_stock)
        stock_model = await self.repository.get_by_stock_symbol(
            stock_input.stock_symbol
        )
        stock_agg = StockAggregate(stock_model)
        validation = await stock_agg.get_stock()
        self.redis.set_item(stock_input.stock_symbol, validation.model_dump_json())
        return validation

    async def post_purchase_stock(self, stock_symbol: str, amount: int) -> int:
        """
        Args:
            stock_symbol (str): The symbol of the stock to purchase.
            amount (int): The number of shares to purchase.

        Returns:
            int: The amount of shares successfully purchased.
        """
        stock_model = await self.repository.post_purchase_order(stock_symbol, amount)
        stock_agg = StockAggregate(stock_model)
        validation = await stock_agg.add_purchase_order()
        return validation.purchased_amount
