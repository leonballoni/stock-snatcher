from infra.repository.external.mkt_watch import MarketWatchRepository
from infra.repository.external.polygon import PolygonRepository
from infra.schema import PostStockExtractorInput


class ExtractorService:

    def __init__(
        self,
        input_params: PostStockExtractorInput,
        market_watch: MarketWatchRepository,
        polygon: PolygonRepository,
    ):
        self.input_params = input_params
        self.polygon_repo = polygon
        self.mkt_watch = market_watch

    def check_stocks_to_update(self):
        pass

    def add_stock(self):
        pass

    def add_competitors(self):
        pass

    def add_market_cap(self):
        pass

    def add_performance(self):
        pass

    def add_stock_values(self):
        pass

    def execute(self):
        pass
