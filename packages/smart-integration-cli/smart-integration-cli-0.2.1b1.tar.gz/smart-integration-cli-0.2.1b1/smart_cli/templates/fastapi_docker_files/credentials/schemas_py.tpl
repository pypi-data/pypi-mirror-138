from typing import List
from pydantic import BaseModel, Field
from enum import Enum

from app.core.schemas import BasePaginationSchema


class CreateCredentialSchema(BaseModel):
    access_token: str
    client_service_id: str
    login: str


class CredentialDetailScheme(BaseModel):
    id: str = Field(..., alias='_id')
    user_id: str
    main_user: str
    platform_id: str


class CredentialCreatedScheme(BaseModel):
    id: str
    platform_id: str


class CredentialPaginationSchema(BasePaginationSchema):
    results: List[CredentialDetailScheme]
