from typing import Annotated, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, Request, status, HTTPException
from seedwork.app.base import (
    GetOneService,
    GetManyService,
    PostService,
    PutService,
    DeleteService,
)
from seedwork.infra.defaults.base import Base
from seedwork.infra.repository.base import (
    GetOneRepository,
    GetManyRepository,
    PostRepository,
    PutRepository,
    DeleteRepository,
)
from seedwork.infra.schemas.base import (
    GetGenericInput,
    GetGenericOutput,
    DeleteGenericOutput,
)


class GetApi:
    async def get_many_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: GetGenericOutput,
        input_params: Annotated[GetGenericInput, Depends()],
    ) -> BaseModel:
        try:
            url = request.url
            input_params._actual_page = f"{url.path}?{url.query}"
            usecase = GetManyService(
                GetManyRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output
        except Exception as exp:
            detail = f"Get API error {str(exp)}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    async def get_one_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: BaseModel,
        input_params: BaseModel = Depends(),
    ) -> BaseModel:
        try:
            usecase = GetOneService(
                GetOneRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output
        except Exception as exp:
            detail = f"Get API error {str(exp)}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class PostApi:
    async def post_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: BaseModel,
        input_params: BaseModel,
    ):
        try:
            usecase = PostService(
                PostRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output.model_dump()
        except Exception as exp:
            detail = f"Post API error {str(exp)}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class PutApi:
    async def put_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: BaseModel,
        input_params: BaseModel,
    ):
        try:
            usecase = PutService(
                PutRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output.model_dump()
        except Exception as exp:
            detail = f"Post API error {str(exp)}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class DeleteApi:
    async def delete_route(
        self,
        request: Request,
        model: Type[Base],
        session: Session,
        output_param: DeleteGenericOutput,
        input_params: BaseModel = Depends(),
    ):
        try:
            usecase = DeleteService(
                DeleteRepository(model, input_params, output_param, session)
            )
            output = await usecase.execute()
            return output.model_dump()
        except Exception as exp:
            detail = f"Post API error {str(exp)}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
