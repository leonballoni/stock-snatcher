from seedwork.infra.schemas import PydanticModel
from datetime import datetime
from seedwork.infra.utils.timezone import tz


class HealthOutput(PydanticModel):
    "Is app alive?"
    datetime: str = datetime.now(tz=tz).strftime("%d-%m-%Y %H:%M:%S")
    status: str = "ok"
    environment: str
