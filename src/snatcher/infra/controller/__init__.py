from modules import AppModule
from seedwork.singleton import BaseSingleton
from settings import Config
from fastapi import FastAPI


class APIBuilder(metaclass=BaseSingleton):
    description = """
# Serviço de API para Stock Snatcher

## Funções:

> **ROUTE**: / <br>
> **MÉTODO**: GET - Health check do app

> **ROUTE**: /stock/{stock_code} <br>
> **MÉTODO**: GET - Recuperar dados de ação

> **ROUTE**: /stock/{stock_code} <br>
> **MÉTODO**: POST - inserir/atualizar pedidos de compra de ação

> **ROUTE**: /extractor <br>
> **MÉTODO**: POST - Atualizar o conjunto de dados da app

"""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._init_api_v1()

    def _init_api_v1(self):
        app_v1 = FastAPI(
            description=self.description,
            summary="Capturador de dados de ações",
            title="Stock Snatcher APP",
            version=self.cfg.APP_VERSION,
            root_path="/api/v1",
        )
        AppModule(app_v1, self.cfg)
        self.app = app_v1
