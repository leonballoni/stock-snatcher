from seedwork.singleton import BaseSingleton
from settings import Config
from fastapi import FastAPI


class APIBuilder(metaclass=BaseSingleton):
    description = """
    # Serviço de API para Stock Snatcher
    
    ## Funções:
    > GET: Recuperar dados de ação
    
    > POST: inserir/atualizar pedidos de compra de ação
    """

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.app = FastAPI(
            description=self.description,
            summary="Capturador de dados de ações",
            title="Stock Snatcher APP",
            version=cfg.APP_VERSION,
            root_path="/api",
        )

    def _v1_api(self, api_path: str = "/v1"):
        pass

    def build_stack(self):
        self._v1_api()
