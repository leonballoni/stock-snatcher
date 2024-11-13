from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    ValidationError,
    ValidationInfo,
    field_validator,
    EmailStr,
    model_validator,
)
from seedwork.infra.utils.timezone import tz


class PydanticModel(BaseModel):
    "BaseModel standard for every schema class"
    model_config = ConfigDict(from_attributes=True)


class CreatedModel(BaseModel):
    """
    Inherits from BaseModel class, defining created_at field.
    """

    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=tz))


class UpdatedModel(CreatedModel):
    """
    Inherits from BaseModel class, defining created_at field.
    """

    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=tz))


class GetInput(PydanticModel):
    "Base pydantic model for GET"
    page: Optional[int] = Field(default=1, gt=0)
    page_size: Optional[int] = Field(default=20, gt=0, le=100)
    _actual_page: Optional[str] = PrivateAttr(default="/")


class SortInput(PydanticModel):
    "Criar método para ordenar por campo ou campos especificados na inserção"

    ...
