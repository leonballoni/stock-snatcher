from datetime import date, datetime
from typing import Tuple

from loguru import logger
from sqlalchemy import asc, desc, inspect


class ModelUtils:
    """SQLalchemy RDS Model oriented utilitarians"""

    def __init__(self, model):
        self.model = model

    def __bool_handler(self, value: str) -> int:
        if value.lower() == "false":
            return 0
        if value.lower() == "true":
            return 1
        return value

    def __datetime_handler(
        self, value: str, date_type: date | datetime
    ) -> datetime | date:
        if isinstance(date_type, datetime):
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        value = datetime.strptime(value, "%Y-%m-%d")
        return value

    def order_by_conditions(self, kwargs: dict) -> Tuple[list, dict]:
        order_by = []
        for column, order in kwargs.items():
            if order == "asc":
                order_by.append(asc(column))
                kwargs.pop({column})
            elif order == "desc":
                order_by.append(desc(column))
                kwargs.pop({column})
        return order_by, kwargs

    def convert_model_attributes(self, kwargs: dict) -> dict:
        "Converte os kwargs retornados para o tipo especificado pelo modelo"
        converted_kwargs = {}
        for key, value in kwargs.items():
            attr_type = getattr(self.model, key).type.python_type
            try:
                if attr_type is bool:
                    value = self.__bool_handler(value)
                if attr_type is date or attr_type is date:
                    converted_value = self.__datetime_handler(value, attr_type)
                else:
                    converted_value = attr_type(value)
                converted_kwargs[key] = converted_value
            except ValueError as exp:
                logger.error(exp)
                raise ValueError(
                    f"Could not convert {key} to {attr_type.__name__}. >>> {exp}"
                )
        return converted_kwargs

    def check_model_types(self, kwargs: dict) -> None:
        "Adicionar um kwarg checker que confere se o tipo encaminhado atende ao critério do modelo para criar exceção do tipo TypeError"
        inspector = inspect(self.model)
        attr_names = [column_attr.key for column_attr in inspector.mapper.column_attrs]

        for key, value in kwargs.items():
            if key in attr_names:
                attr_type = type(getattr(self.model, key))
                assert isinstance(
                    value, attr_type
                ), f"Expected type {attr_type.__name__} for {key}, got {type(value).__name__}"

    def check_model_kwargs(self, kwargs: dict) -> None:
        "Confere se os kwargs utilizados existem no modelo utilizado. Se não retorna erro de atributo"
        inspector = inspect(self.model)
        attr_names = [column_attr.key for column_attr in inspector.mapper.column_attrs]
        for key in kwargs.keys():
            if key not in attr_names or key == "dt_start" or key == "dt_end":
                logger.error("Key is not present at the model`s attributes")
                raise AttributeError(
                    f"The inserted key {key} is not present at the Model {self.model.__tablename__}"
                )
