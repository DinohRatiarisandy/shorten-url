from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.messages import MESSAGES, make_error_page


async def http_exception_handler(request: Request, exc: Exception):
    http_exc = exc if isinstance(exc, HTTPException) else HTTPException(500)
    if request.url.path.startswith("/links"):
        return JSONResponse(
            content={"detail": http_exc.detail}, status_code=http_exc.status_code
        )
    message = MESSAGES.get(http_exc.status_code, http_exc.detail)
    return HTMLResponse(
        content=make_error_page(http_exc.status_code, message),
        status_code=http_exc.status_code,
    )


async def starlette_exception_handler(request: Request, exc: Exception):
    http_exc = (
        exc if isinstance(exc, StarletteHTTPException) else StarletteHTTPException(500)
    )
    if request.url.path.startswith("/links"):
        return JSONResponse(
            content={"detail": http_exc.detail}, status_code=http_exc.status_code
        )
    message = MESSAGES.get(http_exc.status_code, str(http_exc.detail))
    return HTMLResponse(
        content=make_error_page(http_exc.status_code, message),
        status_code=http_exc.status_code,
    )
