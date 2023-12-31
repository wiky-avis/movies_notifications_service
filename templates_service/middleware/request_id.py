from http import HTTPStatus
from uuid import uuid4

from admin_panel_old.settings import settings
from fastapi import Request
from fastapi.responses import JSONResponse


class RequestIdMiddleware:
    async def __call__(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-Id")
        if request_id is None:
            if settings.debug:
                request.headers.__dict__["_list"].append(
                    (
                        "x-request-id".encode(),
                        f"{str(uuid4())}".encode(),
                    )
                )
            else:
                return JSONResponse(
                    content={"message": "Missing X-Request-Id header"},
                    status_code=HTTPStatus.BAD_REQUEST,
                )

        response = await call_next(request)
        return response
