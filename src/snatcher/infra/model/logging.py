from seedwork.infra.defaults import AbstractModel
from sqlalchemy.orm import Mapped
from sqlalchemy import String, JSON
from sqlalchemy.orm import mapped_column
from seedwork.infra.defaults.base import Base


class Logger(Base, AbstractModel):
    __tablename__ = "logs"
    log_request_id: Mapped[int] = mapped_column(primary_key=True)
    endpoint: Mapped[str] = mapped_column(String(250))
    method: Mapped[str] = mapped_column(String(10))
    function_name: Mapped[str] = mapped_column(String(100))
    status_code: Mapped[int]
    body: Mapped[dict] = mapped_column(JSON, nullable=True)
    response: Mapped[dict] = mapped_column(JSON, nullable=True)
    comment: Mapped[str] = mapped_column(String(255), nullable=True)
    requester: Mapped[dict] = mapped_column(JSON, nullable=False)
    latency: Mapped[float]
