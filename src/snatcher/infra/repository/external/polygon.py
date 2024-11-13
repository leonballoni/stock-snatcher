from datetime import datetime
from sqlalchemy.orm import Session
from infra.exception import PydanticValidationError
from infra.exception.http import ErrorHandler
from infra.repository import AbsPoligyonRepository
from settings import Config
import httpx
from infra.schema.external import PolygonSchema


class PolygonRepository(AbsPoligyonRepository):

    def __init__(self, session: Session, config: Config):
        self.session = session
        self.cfg = config

    async def get_daily_open_close(
        self, stock_symbol: str, specific_date: datetime.date
    ) -> PolygonSchema:
        url = f"https://api.polygon.io/v1/open-close/{stock_symbol}/{specific_date.strftime('%Y-%m-%d')}"
        header = {"Authorization": f"Bearer {self.cfg.POLYGON_API_KEY}"}
        response = await self.__get_request(url, header)
        if response.status_code != 200:
            ErrorHandler.handle_pydantic_validation_error(
                PydanticValidationError("Polygon Pydantic validation failed")
            )
        data = PolygonSchema(**response.json())
        return data

    async def __get_request(self, url: str, header: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=url, headers=header)
            except httpx.RequestError as exp:
                ErrorHandler.handle_polygon_api_failed_request(
                    response.status_code, exp
                )
            return response
