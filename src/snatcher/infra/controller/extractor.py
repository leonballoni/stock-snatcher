from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.extractor import ExtractorService
from infra.controller.generic import GenericApi
from infra.model.database import DatabaseSession
from infra.repository.external.polygon import PolygonRepository
from infra.repository.external.mkt_watch import MarketWatchRepository
from infra.schema import PostStockExtractorOutput, PostStockExtractorInput
from settings import Config
from pydantic import Field
from typing import Annotated


class ExtractorController(GenericApi):
    def __init__(self, config: Config, *args, **kwargs):
        tags = ["Data Extractor"]
        prefix = "/extractor"
        self.cfg = config
        super().__init__(tags=tags, prefix=prefix, *args, **kwargs)

        self.add_api_route(
            path="/",
            endpoint=self.add_new_data,
            methods=["POST"],
            response_model=PostStockExtractorOutput,
            responses={
                404: {"description": "No Stock to add."},
                500: {
                    "description": (
                        "Internal Server Error. Possible reasons include:\n",
                        "2. Database Failure",
                    )
                },
            },
        )

    async def add_new_data(
        self,
        input_param: Annotated[
            PostStockExtractorInput,
            Field(description="Stock data extraction requester"),
        ],
        session: Session = Depends(DatabaseSession()),
    ):
        """
        Add fresh stock data to entities

        - **XXXXXX**: xxxxxxx

        **Returns**:
        - A JSON object with the volume of entities added and some descriptive stats
        - HTTP 404 if no item was updated
        - HTTP 500 if there is an internal server error.

        """
        try:
            service = ExtractorService(
                input_param,
                MarketWatchRepository(session),
                PolygonRepository(session, self.cfg),
            )
            response = service.execute()
            return response
        except Exception as exp:
            raise exp
