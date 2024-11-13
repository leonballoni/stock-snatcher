from fastapi import FastAPI

from infra.controller.stock import StockController
from infra.controller.base import BaseController
from infra.controller.extractor import ExtractorController
from settings import Config
from seedwork.singleton import BaseSingleton


class AppModule(metaclass=BaseSingleton):
    """
    AppModule is a singleton class responsible for managing and registering controllers in a FastAPI application.

    Attributes:
        app (FastAPI): The FastAPI application instance.
        cfg (Config): Configuration settings used by the controllers.

    Methods:
        __init__(app: FastAPI, cfg: Config):
            Initializes the AppModule with the given FastAPI app and configuration.

        _build_controller():
            Registers all controllers required by the application.

        _register_controller(controller_cls):
            Registers a single controller by creating an instance and including its router in the application.
    """

    def __init__(self, app: FastAPI, cfg: Config):
        self.cfg = cfg
        self.app = app
        self._build_controller()

    def _build_controller(self):
        self._register_controller(StockController)
        self._register_controller(BaseController)
        self._register_controller(ExtractorController)

    def _register_controller(self, controller_cls):
        instance = controller_cls(self.cfg)
        self.app.include_router(router=instance)
