from pydantic import BaseModel
from seedwork.infra.repository.base import (
    GenericRepository,
    GetOneRepository,
    GetManyRepository,
    PostRepository,
    PutRepository,
    DeleteRepository,
)


class GenericService:

    def __init__(
        self,
        repository: GenericRepository,
    ):
        self.repo: GenericRepository = repository

    async def execute(self) -> BaseModel:
        try:
            return await self.repo.case()
        except Exception as exp:
            raise exp


class GetOneService(GenericService):

    def __init__(self, repository: GetOneRepository):
        super().__init__(repository)


class GetManyService(GenericService):

    def __init__(self, repository: GetManyRepository):
        super().__init__(repository)


class PostService(GenericService):

    def __init__(self, repository: PostRepository):
        super().__init__(repository)


class PutService(GenericService):

    def __init__(self, repository: PutRepository):
        super().__init__(repository)


class DeleteService(GenericService):

    def __init__(self, repository: DeleteRepository):
        super().__init__(repository)
