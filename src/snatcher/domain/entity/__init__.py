from datetime import date


class CompetitorEntity:
    def __init__(self, name: str):
        self.name = name


class StockEntity:
    def __init__(
        self,
        status: str,
        purchased_amount: int,
        purchased_status: str,
        request_date: date,
    ):
        self.status = status
        self.purchased_amount = purchased_amount
        self.purchased_status = purchased_status
        self.request_date = request_date


class StockCompanyEntity:
    def __init__(self, code: str, name: str, url: str, sector: str):
        self.code = code
        self.name = name
        self.url = url
        self.sector = sector
