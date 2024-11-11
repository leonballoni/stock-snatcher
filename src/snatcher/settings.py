from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    Field,
    ValidationError,
    model_validator,
)
from loguru import logger
import os

from seedwork.singleton import BaseSingleton


class Config(BaseSettings, metaclass=BaseSingleton):
    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", env_ignore_empty=True
    )

    ENVIRONMENT: str = Field(
        default="develop", description="Ambiente que foi ativado no projeto"
    )
    APP_VERSION: str = Field(default="0.1.0", description="Versão da aplicação")
    REDIS_URL: str = Field(..., description="URL de conexão do Redis")
    REDIS_PASSWORD: str = Field(..., description="Senha do Redis")

    PSQL_USER: str = Field(..., description="Usuário do PostgreSQL")
    PSQL_PWD: str = Field(..., description="Senha do PostgreSQL")
    PSQL_DB: str = Field(..., description="Nome do banco de dados PostgreSQL")
    DATABASE_URL: str = Field(
        default=f"postgresql+psycopg2://{os.getenv('PSQL_USER')}:{os.getenv('PSQL_PWD')}@postgres:5432/{os.getenv('PSQL_DB')}",
        description="URL de conexão do banco de dados PostgreSQL",
    )

    AIRFLOW__CORE__EXECUTOR: str = Field(..., description="Executor do Airflow")
    AIRFLOW__CORE__SQL_ALCHEMY_CONN: str = Field(
        default=f"postgresql+psycopg2://{os.getenv('PSQL_USER')}:{os.getenv('PSQL_PWD')}@postgres:5432/{os.getenv('PSQL_DB')}",
        description="URL de conexão do banco de dados do Airflow",
    )
    AIRFLOW__CELERY__BROKER_URL: str = Field(
        ..., description="URL do broker do Airflow"
    )
    AIRFLOW__CELERY__RESULT_BACKEND: str = Field(
        default=f"postgresql+psycopg2://{os.getenv('PSQL_USER')}:{os.getenv('PSQL_PWD')}@postgres:5432/{os.getenv('PSQL_DB')}",
        description="Backend de resultados do Celery",
    )
    AIRFLOW__CORE__FERNET_KEY: str = Field(..., description="Chave Fernet do Airflow")
    AIRFLOW__WEBSERVER__PORT: int = Field(
        default=8080, description="Porta do servidor web do Airflow"
    )

    AIRFLOW_ADMIN_USERNAME: str = Field(
        ..., description="Nome de usuário do admin do Airflow"
    )
    AIRFLOW_ADMIN_PASSWORD: str = Field(..., description="Senha do admin do Airflow")
    AIRFLOW_ADMIN_FIRSTNAME: str = Field(
        ..., description="Primeiro nome do admin do Airflow"
    )
    AIRFLOW_ADMIN_LASTNAME: str = Field(
        ..., description="Último nome do admin do Airflow"
    )
    AIRFLOW_ADMIN_EMAIL: str = Field(..., description="Email do admin do Airflow")

    @model_validator(mode="before")
    @classmethod
    def model_validation(cls, values: dict):
        try:
            if values.get("ENVIRONMENT") == "test":
                values["DATABASE_URL"] = (
                    f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'TESTE.db'))}"
                )
            return values
        except ValidationError as exp:
            raise ValueError(f"SMTP PORT com valor inadequado: {exp}") from exp


cfg = Config()

logger.info(
    f"Started {cfg.ENVIRONMENT} environment. Acessing {cfg.DATABASE_NAME} database at ***{cfg.DATABASE_URL[0:11]}***"
)
