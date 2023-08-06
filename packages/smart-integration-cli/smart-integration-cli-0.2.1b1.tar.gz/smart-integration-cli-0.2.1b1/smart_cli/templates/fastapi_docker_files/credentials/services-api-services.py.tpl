from logging import getLogger
from fastapi import HTTPException
from integration_tools.crypt import decode, encode
from app.core.services.api_services import BaseServiceManager

from .models import Credential
from .schemas import CreateCredentialSchema


logger = getLogger(__name__)


class CredentialService(BaseServiceManager):
    async def create_or_update_credential(self, create_schema: CreateCredentialSchema) -> Credential:
        raise NotImplementedError('implement create or update credential')


credential_service = CredentialService(Credential)