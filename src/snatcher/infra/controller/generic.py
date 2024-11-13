from fastapi import APIRouter, Depends
from typing import Optional, List
from infra.controller.logging import LogAPIRoute
from loguru import logger


class GenericApi(APIRouter):
    """
    Define a generic API router with logging and authentication requirements.

    This class initializes a router that logs all requests and enforces authentication for each request.

    Args:
        custom_dependencies: list of additional dependencies besides authentication
    """

    def __init__(self, custom_dependencies: Optional[List[Depends]] = None, *args, **kwargs):
        try:
            dependencies = []
            if custom_dependencies:
                dependencies += custom_dependencies
            super().__init__(route_class=LogAPIRoute, dependencies=dependencies, *args, **kwargs)
        except Exception as error:
            logger.error(f"Error during APIRouter initialization: {error}")
