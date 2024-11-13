from fastapi import APIRouter

from infra.controller.generic import GenericApi
from seedwork.infra.schemas.health import HealthOutput
from settings import Config


class BaseController(GenericApi):

    def __init__(self, config: Config, *args, **kwargs):
        self.cfg = config
        super().__init__(*args, **kwargs)

        self.add_api_route(
            path="/",
            endpoint=self.get_health_checked,
            methods=["GET"],
            response_model=HealthOutput,
        )

    def get_health_checked(self):
        return HealthOutput(environment=self.cfg.ENVIRONMENT)
