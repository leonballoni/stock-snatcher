from typing import List

from seedwork.infra.schemas.pagination import (
    PageLink,
    PageMeta,
    PageResult,
    PydanticModel,
)
from infra.typing.pagination import Items
from sqlalchemy.orm import Query


class Pagination:
    def __init__(
        self, query: Query, page: int, page_size: int, actual_page: str
    ) -> None:
        if page <= 0 or page_size <= 0:
            raise ValueError("Page and page_size must be positive integers.")

        self.query: Query = query
        self.page: int = page
        self.page_size: int = page_size
        self.actual_page: str = actual_page
        self.total_items: int = self.query.count()

        if self.page_size > 0 and not self.page == -1:
            self.total_pages: int = (
                self.total_items + self.page_size - 1
            ) // self.page_size
        else:
            self.total_pages: int = 1  # Handle case where page_size is 0 or negative

        self._fetch_items()

    def _fetch_items(self) -> None:
        self.items = (
            self.query.offset((self.page - 1) * self.page_size)
            .limit(self.page_size)
            .all()
            if self.page_size > 0 and self.page > 0
            else self.query.all()
        )

        self.page_meta = {
            "page": self.page,
            "page_size": self.page_size,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
        }
        self.url_meta = {
            "next_page": self.next_page,
            "prev_page": self.prev_page,
            "actual_page": self.actual_page,
        }

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        if self.has_next:
            base_url = self.actual_page.split("?")[0]

            existing_params = self.actual_page.split("?")[1].split("&")
            preserved_params = [
                param
                for param in existing_params
                if not param.startswith("page=") and not param.startswith("page_size=")
            ]

            next_page_url = f"{base_url}?{'&'.join(preserved_params)}&page={self.page + 1}&page_size={self.page_size}"
            return next_page_url
        return None

    @property
    def prev_page(self):
        if self.has_prev:
            base_url = self.actual_page.split("?")[0]

            existing_params = self.actual_page.split("?")[1].split("&")
            preserved_params = [
                param
                for param in existing_params
                if not param.startswith("page=") and not param.startswith("page_size=")
            ]

            next_page_url = f"{base_url}?{'&'.join(preserved_params)}&page={self.page - 1}&page_size={self.page_size}"
            return next_page_url
        return None

    def to_pydantic_schema(self, item_schema: PydanticModel) -> PageResult:
        return PageResult(
            items=item_schema(**self.items),
            links=PageLink(**self.url_meta),
            meta=PageMeta(**self.page_meta),
        )

    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "page_size": self.page_size,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "items": self.items,
            "next_page": self.next_page,
            "prev_page": self.prev_page,
            "actual_page": self.actual_page,
        }

    @classmethod
    def paginate_to_dict(cls, query, page, page_size, actual_page) -> dict:
        pagination = cls(query, page, page_size, actual_page)
        return pagination.to_dict()

    @classmethod
    def paginate_to_pydantic(
        cls, query, page, page_size, actual_page, item_schema: PydanticModel
    ) -> PageResult:
        pagination = cls(query, page, page_size, actual_page)
        return pagination.to_pydantic_schema(item_schema)
