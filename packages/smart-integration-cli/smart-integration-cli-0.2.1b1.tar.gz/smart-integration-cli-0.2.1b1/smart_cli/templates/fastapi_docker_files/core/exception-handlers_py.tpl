from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse(
            {"success": False, "data": {"detail": exc.detail}},
            status_code=exc.status_code,
            headers=headers,
        )
    else:
        return JSONResponse(
            {"success": False, "data": {"detail": exc.detail}},
            status_code=exc.status_code,
        )


async def custom_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "data": {"detail": jsonable_encoder(exc.errors())}},
    )
