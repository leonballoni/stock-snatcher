from fastapi import APIRouter
from pydantic import BaseModel

class StockOutput(BaseModel):
    pass

class StockBuyOrderOutput(BaseModel):
    pass

class StockController(APIRouter):
    tags = [""]
    prefix = "/stock"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_api_route(
            path="/{stock_symbol}",
            endpoint=self.get_stock,
            methods=['GET'],
            response_model=StockOutput,
        )
        self.add_api_route(
            path="/{stock_symbol}",
            endpoint=self.post_stock,
            methods=['POST'],
            response_model=StockBuyOrderOutput,
        )


    def get_stock(self): ...

    def post_stock(self): ...
