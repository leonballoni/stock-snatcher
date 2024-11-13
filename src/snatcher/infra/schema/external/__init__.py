from datetime import date

from seedwork.infra.schemas import PydanticModel, Field


class PolygonSchema(PydanticModel):
    status: str
    from_date: date = Field(alias="from")
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    after_hours: float = Field(alias="afterHours")
    pre_market: float = Field(alias="preMarket")
