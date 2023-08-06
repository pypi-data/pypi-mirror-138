from typing import Any, List, Type
from fastapi import HTTPException, Request

from .paginator import Paginator, DefaultSchema


class BaseServiceManager(object):
    def __init__(
        self, model: Any,
    ):
        self.model = model

    def create_object(self, *args, **kwargs) -> dict:
        raise NotImplementedError()

    def _validate_params(self, limit_rows: int, skip_rows: int, **kwargs) -> dict:
        if limit_rows <= 0:
            raise HTTPException(status_code=422, detail='invalid limit param.')
        if skip_rows < 0:
            raise HTTPException(status_code=422, detail='invalid offset param.')
        params = {'skip_rows': skip_rows, 'limit_rows': limit_rows}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return params

    def _pagenate_response(
        self,
        request: Request,
        count: int,
        data: list,
        schema: DefaultSchema,
        limit_rows: int,
        skip_rows: int,
    ):
        paginator = Paginator(request, count, data, schema, limit_rows, skip_rows)
        return paginator.response()

    async def get_objects(
        self, request: Request, schema: Any, limit_rows: int, skip_rows: int, **kwargs,
    ) -> Any:
        raise NotImplementedError()
        #return self._pagenate_response(
        #    request, count, qs.data, schema, limit_rows, skip_rows
        #)

    async def get_object(self, object_id: str):
        raise NotImplementedError()

    async def delete_object(self, object_id: str):
        raise NotImplementedError()

    def update_object(self, object_id: str, obj: Any):
        raise NotImplementedError()

    async def delete_many_objects(self, object_ids: List[str]):
        raise NotImplementedError()
