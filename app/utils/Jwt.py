from ast import Dict
from typing import Any, cast
import jwt
import datetime
from decouple import config

from app.interfaces.JwtUtils import HeaderPayloadTH
from fastapi.responses import JSONResponse

from app.utils.excpetions import JwtValidationError

SECRET_KEY = cast(str, config("SECRET_KEY"))


class JwtUtils:
    @staticmethod
    def get_secret_key() -> str:
        return SECRET_KEY

    @classmethod
    def create_jwt_token(cls, payload: Any):
        secret_key = cls.get_secret_key()
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    @classmethod
    def create_jwt_response(
        cls, user: HeaderPayloadTH, message="Login successful", status_code=200
    ) -> JSONResponse:
        user["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=7
        )
        token = cls.create_jwt_token(user)
        response = JSONResponse(
            status_code=201,
            content={"token": token, "message": message},
        )
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=True,
            secure=True,
            samesite="none",  # Changed for cross-site + incognito support
            max_age=7 * 24 * 60 * 60,
            path="/",  # Optional but recommended
        )
        return response

    @classmethod
    def validate_token(
        cls,
        token: str,
    ) -> HeaderPayloadTH:
        try:
            JWT_ALGORITHM = "HS256"
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except Exception:
            raise JwtValidationError("Error  in ValidatiNG  jwt Token ...")
