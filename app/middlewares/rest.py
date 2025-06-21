from typing import FrozenSet
import uuid
from starlette.types import ASGIApp
from app.context.vars import headers_context
from app.interfaces.Context import Headers_PM
from app.utils.Jwt import JwtUtils
from app.utils.excpetions import JwtValidationError
from pydantic import ValidationError


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
