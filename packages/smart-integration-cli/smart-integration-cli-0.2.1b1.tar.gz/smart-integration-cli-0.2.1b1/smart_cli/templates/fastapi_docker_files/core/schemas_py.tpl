from typing import Optional, Any, Union, List, Optional
from pydantic import BaseModel


class BasePaginationSchema(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: Any


class DefaultResponseSchema(BaseModel):
    success: bool = True
    message: str


class SelectionValueSchema(BaseModel):
    code: Union[str, int]
    value: str
    enums: list = []


class SelectionSchema(BaseModel):
    code: Union[str, int]
    name: str
    enums: List[Optional['SelectionValueSchema']] = []


class FilterSchema(BaseModel):
    code: Union[str, int]
    name: str
