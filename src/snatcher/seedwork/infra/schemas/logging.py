from typing import Optional, Union

from seedwork.infra.schemas import UpdatedModel
from pydantic import ConfigDict, Field


class LogRequestOutput(UpdatedModel):
    endpoint: Optional[str] = None
    method: Optional[str] = Field(None, max_length=10)
    function_name: Optional[str] = Field(None, max_length=100)
    status_code: Optional[int] = None
    body: Optional[Union[dict, str, list]] = None
    response: Optional[Union[dict, list, str]] = None
    comment: Optional[str] = Field(None, max_length=255)
    requester: Optional[Union[dict, str, list]] = None
    latency: Optional[float] = None
    model_config = ConfigDict(title="log_request", from_attributes=True)


class LogError(UpdatedModel):
    status_code: Optional[int] = None
    method: str
    response: Optional[Union[dict, str]] = None
    counter: Optional[int] = None
    body: Optional[Union[dict, str]] = None
    endpoint: str
    user: Optional[dict] = None
    error: str
    requester: Optional[Union[dict, str, list]] = None
