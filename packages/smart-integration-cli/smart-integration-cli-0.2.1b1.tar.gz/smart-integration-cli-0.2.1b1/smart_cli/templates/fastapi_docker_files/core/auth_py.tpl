import os
from typing import Optional, no_type_check
from importlib import import_module
from urllib.parse import unquote_plus

from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.api_key import (
    APIKeyBase,
    APIKey,
    APIKeyIn,
)
from fastapi.security.oauth2 import get_authorization_scheme_param


from integration_tools.api import BaseCredentialMixin
from integration_tools.exceptions import PermissionDenied

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.settings'))
credential_module_path, credential_model_name = settings.CREDENTIAL_MODEL.rsplit('.', 1)  # type: ignore
module = import_module(credential_module_path)

__all__ = ('authorize_to_smart',)


class SmartAuth(BaseCredentialMixin):
    pass


class SmartHTTPToken(APIKeyBase):
    def __init__(
        self,
        *,
        name: str,
        scheme_name: Optional[str] = None,
        auto_error: bool = True,
        oauth_model: str = None,
    ):
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name=name)
        self.oauth_model: APIKey = APIKey(
            **{"in": APIKeyIn.query}, name=oauth_model or 'token'
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def _check_auth(
        self, authorization: str
    ) -> Optional[HTTPAuthorizationCredentials]:
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=403,
                    detail="Permission Denied",
                )
            else:
                return None
        if scheme.lower() not in ("token",):
            if self.auto_error:
                raise HTTPException(
                    status_code=403,
                    detail="Permission Denied",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        if request.query_params.get(self.oauth_model.name):
            return await self._check_auth(
                unquote_plus(request.query_params[self.oauth_model.name])
            )
        else:
            return await self._check_auth(request.headers.get(self.model.name))


@no_type_check
async def authorize_to_smart(
    platform_id: str,
    auth: HTTPAuthorizationCredentials = Security(
        SmartHTTPToken(
            name='Authorization',
            scheme_name='Smart Authorization token',
            oauth_model='token',
        )
    ),
) -> dict:
    if platform_id not in ('dev', 'prod'):
        raise HTTPException(
            status_code=403,
            detail=f"Permission Denied, invalid platform_id, platform_id must in (dev, prod), not {platform_id}",
        )
    smart_auth = SmartAuth()
    try:
        user_info = await smart_auth.get_user_info_async(auth.credentials, platform_id)
        return {
            'smart_user_name': user_info['username'],
            'smart_user_id': user_info['id'],
            'platform_id': platform_id,
        }

    except PermissionDenied as e:
        raise HTTPException(status_code=e.status, detail=e.error_detail)
