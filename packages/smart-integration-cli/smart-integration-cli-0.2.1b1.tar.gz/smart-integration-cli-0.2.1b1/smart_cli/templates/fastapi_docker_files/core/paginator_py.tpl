from typing import Optional, Type
from fastapi import Request

from .schemas import BasePaginationSchema
from .utils import remove_query_param, replace_query_param

DefaultSchema = Type['BasePaginationSchema']


class Paginator(object):
    def __init__(
        self,
        request: Request,
        count: int,
        data: list,
        schema: DefaultSchema,
        limit: int = 100,
        offset: int = 0,
        max_limit: Optional[int] = None,
    ):
        self.request = request
        self.max_limit = max_limit if max_limit else 1000
        self.limit = limit if limit <= self.max_limit else self.max_limit
        self.offset = offset
        self.count = count
        self.schema = schema
        self.data = data

    def get_next_link(self) -> Optional[str]:
        if self.offset + self.limit >= self.count:
            return None

        url = str(self.request.url)
        url = replace_query_param(url, 'limit', self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, 'offset', offset)

    def get_prev_link(self) -> Optional[str]:
        if self.offset <= 0:
            return None

        url = str(self.request.url)
        url = replace_query_param(url, 'limit', self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, 'offset')

        offset = self.offset - self.limit
        return replace_query_param(url, 'offset', offset)

    def response(self):
        return self.schema(
            count=self.count,
            next=self.get_next_link(),
            prev=self.get_prev_link(),
            results=self.data,
        )

