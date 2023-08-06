from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from app.core.depends import get_smart_auth, get_credential as get_credential_depends

from .schemas import CredentialCreatedScheme
from .models import Credential

from .services.api_services import credential_service

api_router = APIRouter()


@api_router.post('/', response_model=CredentialCreatedScheme, status_code=201)
async def create_credentials(
    profile_id: str,
    create_schema: CreateCredentialSchema,
    auth=Depends(get_smart_auth),
):
    credential = await credential_service.create_or_update_credential(
        create_schema, **auth
    )
    return {
        'id': str(credential._id),
        'platform_id': credential.platform_id,
    }