from fastapi.responses import JSONResponse
from app.interfaces.User import Login_PM, SignUp_PM
from app.ioc.ioc import SingletonMeta
from app.services.User import UserService
from app.utils.Jwt import JwtUtils


class UserController(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._user_service = UserService()

    def add_user(self, payload: SignUp_PM) -> JSONResponse:
        self._user_service.user_signup(payload)
        return JSONResponse(status_code=201, content="Succefully Signed  Up User .")

    def login_user(self, payload: Login_PM) -> JSONResponse:
        user = self._user_service.login_user(payload)
        return JwtUtils().create_jwt_response(user)

    def logout_user(self) -> JSONResponse:
        response = JSONResponse(
            status_code=200,
            content={"message": "Successfully logged out."},
        )
        response.delete_cookie(
            key="access_token",
            path="/",
        )
        return response
