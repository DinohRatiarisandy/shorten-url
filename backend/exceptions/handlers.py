from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.messages import MESSAGES

templates = Jinja2Templates(directory="templates")


async def http_exception_handler(request: Request, exc: Exception):
    http_exc = exc if isinstance(exc, HTTPException) else HTTPException(500)
    if request.url.path.startswith("/links"):
        return JSONResponse(
            content={"detail": http_exc.detail}, status_code=http_exc.status_code
        )
    message = MESSAGES.get(http_exc.status_code, http_exc.detail)
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"status_code": http_exc.status_code, "message": message},
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
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"status_code": http_exc.status_code, "message": message},
        status_code=http_exc.status_code,
    )
