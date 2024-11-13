import json
import time
from typing import Callable
from uuid import uuid4

from infra.model.logging import Logger as LogRequest
from fastapi import HTTPException, Request, Response, status
from starlette.datastructures import UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from loguru import logger
from infra.model.database import DatabaseSession
from seedwork.infra.schemas.logging import LogRequestOutput


class LogAPIRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    async def get_request_params(request: Request) -> dict:
        """
        Get body content, evaluating content type or from .body method
        Args:
            request: request object

        Returns:
            query and path params content
        """
        try:
            params = {}
            params.update(dict(request.query_params))
            params.update(request.path_params)
            return params
        except Exception as error:
            logger.error(f"Error to get request params {error}")
            return {}

    async def _get_content_type(self, request: Request):
        # TODO -> simplificar content-type fetch
        if request.method in ("GET", "DELETE"):
            self._content_type = request.headers.get("accept")
            # self._get_params()
        elif request.method in ("POST", "PUT"):
            self._content_type = request.headers.get("content-type").split(";")[0]
            # self._get_form()

    async def _get_request_params(self, request: Request):
        # TODO preparar conjunto de dados de entrada para log antecipadamente
        if request.method in ("GET", "DELETE"):
            query_params = request.query_params._dict
            path_params = request.path_params
        elif request.method in ("POST", "PUT"):
            # TODO -> variará com o content-type
            pass

    @staticmethod
    async def get_request_body(request: Request):
        """
        Get body content, evaluating content type or from .body method
        Args:
            request: request object

        Returns:
            body content
        """
        try:
            # TODO -> refatorar isso para reduzir complexidade lógica! (SOLID e Clean)
            content_type = (
                request.headers.get("content-type")
                if request.headers.get("content-type")
                else request.headers.get("accept")
            )
            content_type = content_type.split(";")[0]
            if content_type in (
                "application/x-www-form-urlencoded",
                "multipart/form-data",
            ):
                form_data = dict(await request.form())
                if isinstance(form_data.get("file"), UploadFile):
                    form_data = {
                        "filename": form_data.get("file").filename,
                        "content_type": form_data.get("file").content_type,
                        "file_size": form_data.get("file").size,
                    }
                return form_data
            elif content_type == "application/json":
                return await request.json()
        except Exception as warning:
            logger.warning(
                f"Warning! request body given content_type: {warning}. Trying get from .body method"
            )
        raw_data = await request.body()
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (TypeError, json.decoder.JSONDecodeError):
            return raw_data.decode("utf-8")

    async def before_route_handler(self, request: Request):
        """
        What to execute before route handler execution.
        Args:
            request: request object

        Returns:
            Return a dict with "before_time" and "log_collection" keys to be used in "after_route_handler" method
        """
        body = None
        try:
            body = await self.get_request_body(request)
            params = await self.get_request_params(request)
            before = time.time()
            return {
                "params": params,
                "body": body,
                "before_time": before,
            }
        except HTTPException as error:
            raise error
        except Exception as error:
            error_msg = f"Error in before_route_handler in LogAPIRoute class: {error}"
            logger.critical(error_msg)

    async def _get_requestor_data(self, request: Request) -> dict:
        header = request.headers
        return {
            "host": header.get("host"),
            "client-host": request.client.host,
            "x-forwarded-for": header.get("x-forwarded-for"),
            "user-agent": header.get("user-agent"),
            "referer": header.get("referer"),
            "content-type": (
                header.get("content-type")
                if header.get("content-type")
                else header.get("accept")
            ),
            "content-length": header.get("content-length"),
            "origin": header.get("origin"),
            "connection": header.get("connection"),
        }

    async def after_route_handler(
        self, request: Request, response, function_name, params, body, before_time
    ):  # -> LogRequest:
        """
        What to execute after route handler execution. Require the return of the "before_route_handler" method with
        keys "before" and "log_collection"
        Args:
            request: request object
            body: body content
            response: response object
            before_time: time before request

        Returns:
            None
        """
        log_response = {}
        logger.info(params if params else None)
        body.pop("password", None) if isinstance(body, dict) else body
        try:
            db_session = DatabaseSession()
            session = next(db_session.get_session())
            duration = time.time() - before_time
            requester = await self._get_requestor_data(request)
            if response.headers is None:
                response.headers = {}
            response.headers["X-Response-Time"] = str(duration)
            if hasattr(response, "body"):
                log_response = json.loads(response.body.decode("utf-8"))
            elif hasattr(response, "detail"):
                log_response = response.detail
            log_request = LogRequestOutput(
                endpoint=str(request.url),
                method=request.method,
                function_name=function_name,
                status_code=response.status_code,
                body=body,
                requester=requester,
                latency=duration,
                response=log_response,
            )
            session.add(LogRequest(**log_request.model_dump()))
            session.flush()
            session.commit()
        except Exception as error:
            error_msg = f"Error in after_route_handler in LogAPIRoute class: {error}"
            logger.critical(error_msg)
            session.rollback()

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def log_route_handler(request: Request) -> Response:
            before_handler_return = await self.before_route_handler(request)

            try:
                response = await original_route_handler(request)
            except HTTPException as error:
                error.detail = f"{error.detail}. Code error: {uuid4()}"
                response = error
            except RequestValidationError as error:
                fields_error = (
                    f"Field(s) {', '.join(x.get('loc', ['', ''])[1] for x in error.args[0])} not valid"
                    if len(error.args) > 0
                    else error
                )
                response = HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Validation error: {fields_error}. Code error: {uuid4()}",
                )
            except Exception as error:
                response = HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error: {error}. Code error: {uuid4()}",
                )
            await self.after_route_handler(
                request=request,
                response=response,
                function_name=self.endpoint.__name__,
                **before_handler_return,
            )
            if isinstance(response, HTTPException):
                raise response
            return response

        return log_route_handler
