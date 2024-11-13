from sqlalchemy.orm import Session
from infra.repository import AbsMarketWatchRepository


class MarketWatchRepository(AbsMarketWatchRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_competitors(self):
        pass

    def get_performance(self):
        pass

    def get_stock_list(self):
        pass
