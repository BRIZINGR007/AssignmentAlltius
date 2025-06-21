import json
import sys
import traceback
from typing import FrozenSet
import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send
from app.context.vars import headers_context
from app.enums.MiscEnums import ServicePaths
from app.interfaces.Context import Headers_PM
from app.utils.Jwt import JwtUtils
from app.utils.excpetions import JwtValidationError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class HeaderValidationMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        x_api_key_1: str,
        x_api_key_2: str,
        excluded_paths: FrozenSet[str] = frozenset(),
    ) -> None:
        self.app = app
        self.x_api_key_1 = x_api_key_1
        self.x_api_key_2 = x_api_key_2
        self.excluded_paths: FrozenSet[str] = frozenset(
            {"/docs", "/openapi.json", *excluded_paths}
        )

    async def validate_headers(self, headers, path: str) -> tuple[bool, dict, int]:
        access_token = None
        # Check for access token in headers
        if "access_token" in headers.get("cookie", ""):
            # Parse cookie string to get access token
            cookies = dict(
                cookie.split("=")
                for cookie in headers.get("cookie", "").split("; ")
                if cookie
            )
            access_token = cookies.get("access_token")
        elif "authorization" in headers:
            access_token = headers["authorization"]

        try:
            if access_token:
                payload = JwtUtils.validate_token(access_token)
                headers_model = Headers_PM(
                    **dict(
                        correlationid=headers.get("correlationid", str(uuid.uuid4())),
                        userId=payload["userId"],
                        email=payload["email"],
                        authorization=access_token,
                    )
                )
                headers_context.set(headers_model)
                return True, {}, 200

            if (
                headers.get("x-api-key-1") == self.x_api_key_1
                or headers.get("x-api-key-2") == self.x_api_key_2
            ):
                headers_model = Headers_PM(
                    **dict(
                        correlationid=headers.get("correlationid", str(uuid.uuid4())),
                        username=headers.get("username", ""),
                        authorization=headers.get("authorization", ""),
                    )
                )
                headers_context.set(headers_model)
                return True, {}, 200

            return (
                False,
                {"detail": "Unauthorized: Missing or invalid credentials."},
                401,
            )

        except (JwtValidationError, ValidationError) as e:
            return False, {"detail": str(e)}, 401
        except Exception as e:
            return False, {"detail": "Internal server error"}, 500

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ["http", "websocket"]:
            return await self.app(scope, receive, send)

        path = scope["path"]
        if any(path.startswith(excluded_path) for excluded_path in self.excluded_paths):
            return await self.app(scope, receive, send)

        headers = dict(scope["headers"])
        headers = {k.decode(): v.decode() for k, v in headers.items()}

        is_valid, error_detail, status_code = await self.validate_headers(headers, path)

        if not is_valid:
            if scope["type"] == "http":
                response = JSONResponse(error_detail, status_code=status_code)
                return await response(scope, receive, send)
            else:

                async def close_websocket():
                    await send(
                        {
                            "type": "websocket.close",
                            "code": 4000
                            + status_code,  # Using 4000 + HTTP status code as WebSocket close code
                            "reason": error_detail["detail"],
                        }
                    )

                return await close_websocket()

        return await self.app(scope, receive, send)


class ExceptionMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    def log_exception(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback_info = traceback.extract_tb(exc_traceback)
            relevant_traceback = next(
                (
                    trace
                    for trace in reversed(traceback_info)
                    if ServicePaths.AI_SERVICE in trace.filename
                ),
                None,
            )
            if relevant_traceback:
                pathname, lineno, funcName, code_line = relevant_traceback
                error_data = {
                    "exception_type": str(exc_type.__name__),
                    "exception_value": str(exc_value),
                    "pathname": str(pathname),
                    "lineno": str(lineno),
                    "funcName": funcName,
                    "code_line": str(code_line),
                }
                logger.error(json.dumps(error_data))

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        try:
            await self.app(scope, receive, send)

        except HTTPException as http_exception:
            self.log_exception()
            await self.handle_http_exception(http_exception, scope, receive, send)
        except Exception as e:
            self.log_exception()
            await self.handle_internal_server_error(e, scope, receive, send)

    async def handle_http_exception(self, http_exception, scope, receive, send):
        response = JSONResponse(
            {"detail": http_exception.detail},
            status_code=http_exception.status_code,
        )
        await response(scope, receive, send)

    async def handle_internal_server_error(self, exception, scope, receive, send):
        error_message = {
            "detail": "Internal Server Error",
            "error_message": str(exception),
        }
        response = JSONResponse(status_code=500, content=error_message)
        await response(scope, receive, send)
