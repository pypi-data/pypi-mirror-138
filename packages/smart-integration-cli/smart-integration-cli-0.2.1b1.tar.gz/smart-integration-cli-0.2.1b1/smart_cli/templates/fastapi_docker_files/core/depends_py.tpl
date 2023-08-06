import os
from typing import Any, no_type_check
from importlib import import_module

from fastapi import HTTPException
from fastapi.param_functions import Depends

from bson.errors import InvalidId

from .auth import authorize_to_smart

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.settings'))
credential_module_path, credential_model_name = settings.CREDENTIAL_MODEL.rsplit('.', 1)  # type: ignore
module = import_module(credential_module_path)
CREDENTIAL_MODEL = getattr(module, credential_model_name)


@no_type_check
async def get_smart_auth(auth_data: tuple = Depends(authorize_to_smart)):
    return auth_data


@no_type_check
async def get_credential(credential_id: str, _=Depends(get_smart_auth)) -> Any:
    http_exception = HTTPException(
        status_code=403,
        detail="Invalid credential",
    )
    try:
        credential = await CREDENTIAL_MODEL.AQ.find_one(_id=credential_id)
        if not credential:
            raise http_exception
        return credential
    except InvalidId:
        raise http_exception
