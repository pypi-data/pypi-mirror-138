from fastapi import APIRouter, Depends

from .credentials.api import api_router as credentail_api_router

api_router = APIRouter()

api_router.include_router(
    credentail_api_router, tags=["credential"], prefix='/credential',
)
