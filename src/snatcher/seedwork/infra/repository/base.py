from infra.common.sessions import DatabaseSessions
from seedwork.infra.utils.pagination import Pagination
from pydantic import BaseModel
from typing import List, Type
from seedwork.infra.defaults.base import Base
from sqlalchemy.orm import Session
from loguru import logger
from sqlalchemy import desc
from seedwork.infra.utils.filter import Filtering
from seedwork.infra.utils.model import ModelUtils
from seedwork.infra.schemas.pagination import PageResult, PageLink, PageMeta


class GenericRepository:

    def __init__(
        self,
        model: Type[Base] | None | List[Type[Base]],
        input_schema: Type[BaseModel],
        output_schema: Type[BaseModel],
        session: Session,
    ):
        self.pagination = Pagination
        self.filtering = Filtering
        self.database_session = DatabaseSessions()
        self.model = model
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.session = session
        self.repository_utils = ModelUtils
        self._metadata()

    def _metadata(self):
        self.metadata = {
            "model": self.model,
            "primary_key_attr": getattr(
                self.model, f"{self.model.__tablename__}_id", "id"
            ),
            "primary_key_name": self.model.__table__.primary_key.columns.keys()[0],
            "columns": self.model.__table__.columns.keys(),
            "table": self.model.__tablename__,
        }

    async def case(self) -> BaseModel:
        "Atribui o caso de utilizacao do repositório"
        pass


class GetOneRepository(GenericRepository):
    def __init__(
        self,
        model: Type[Base],
        input_schema: BaseModel,
        output_schema: BaseModel,
        session: Session,
    ):

        super().__init__(model, input_schema, output_schema, session)

    async def case(self) -> BaseModel | None:
        query = self.session.query(self.model).order_by(
            desc(self.metadata.get("primary_key_attr"))
        )
        query = self.filtering(query, self.input_schema).query
        output = query.one_or_none()
        if output:
            return self.output_schema.model_validate(output)


class GetManyRepository(GenericRepository):
    def __init__(
        self,
        model: Type[Base],
        input_schema: BaseModel,
        output_schema: BaseModel,
        session: Session,
    ):

        super().__init__(model, input_schema, output_schema, session)

    async def case(self) -> PageResult:
        await self._validated_input()
        query = self.session.query(self.model).order_by(
            desc(self.metadata.get("primary_key_attr"))
        )
        query = self.filtering(query, self.input_schema).query
        output = self.pagination.paginate_to_dict(
            query,
            self.input_schema.page,
            self.input_schema.page_size,
            self.input_schema._actual_page,
        )
        return self.output_schema(
            items=output.get("items"),
            links=PageLink(**output),
            meta=PageMeta(**output),
        )

    async def _validated_input(self):
        try:
            model_utils = self.repository_utils(self.model)
            model_utils.check_model_kwargs(
                self.input_schema.model_dump(
                    exclude={"page", "page_size", "_actual_page"}
                )
            )
        except AttributeError as aterror:
            raise aterror


class PostRepository(GenericRepository):
    def __init__(
        self,
        model: Type[Base],
        input_schema: BaseModel,
        output_schema: BaseModel,
        session: Session,
    ):
        super().__init__(model, input_schema, output_schema, session)

    async def case(self) -> BaseModel:
        insert = self.model(**self.input_schema.model_dump())

        insert = self.database_session.create_session(self.session, insert)
        return self.output_schema.model_validate(insert)


class PutRepository(GenericRepository):
    def __init__(
        self,
        model: Type[Base],
        input_schema: Type[BaseModel],
        output_schema: Type[BaseModel],
        session: Session,
    ):
        super().__init__(model, input_schema, output_schema, session)

    async def case(self) -> BaseModel:
        primary_key = self.metadata.get("primary_key_name")
        put = self.session.query(self.model).filter(
            self.metadata.get("primary_key_attr")
            == getattr(self.input_schema, primary_key)
        )
        to_update = self.input_schema.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={self.metadata.get("primary_key_name")},
        )
        result = put.update(to_update)
        self.database_session.update_session(self.session, put)
        logger.info(f"Rows updated: {result}")
        logger.info(
            f"{self.input_schema.__repr_name__()} with id: {getattr(self.input_schema, primary_key)} changed to {to_update}"
        )
        result = self.session.query(self.model).filter(
            self.metadata.get("primary_key_attr")
            == getattr(self.input_schema, primary_key)
        )
        return self.output_schema.model_validate(result.one_or_none())


class DeleteRepository(GenericRepository):
    def __init__(
        self,
        model: Type[Base],
        input_schema: BaseModel,
        output_schema: BaseModel,
        session: Session,
    ):
        super().__init__(model, input_schema, output_schema, session)

    async def case(self) -> BaseModel:
        delete_id = getattr(self.input_schema, self.metadata.get("primary_key_name"))
        delete = (
            self.session.query(self.model)
            .filter(self.metadata.get("primary_key_attr") == delete_id)
            .one_or_none()
        )
        if not delete:
            logger.error("No item was found to be deleted")
            return self.output_schema(
                **{
                    "status": "nothing to delete",
                    "metadata": {
                        "tablename": self.metadata.get("table"),
                        "id": delete_id,
                    },
                }
            )
        self.database_session.delete_session(self.session, delete)
        logger.info("Row deleted")
        logger.info(
            f"{self.metadata.get('table')} tabled deleted row with id {delete_id}"
        )
        return self.output_schema(
            **{
                "status": "deleted",
                "metadata": {"tablename": self.metadata.get("table"), "id": delete_id},
            }
        )
