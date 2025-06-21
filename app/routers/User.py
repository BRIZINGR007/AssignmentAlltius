from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.controllers.Chat import ChatController
from app.controllers.User import UserController
from app.enums.MiscEnums import ServicePaths
from app.interfaces.User import Login_PM, SignUp_PM

router = APIRouter(
    prefix=ServicePaths.CONTEXT_PATH.value + "/user",
    tags=["user"],
    responses={"404": {"description": "Not found"}},
)


@router.post("/no-check/login")
async def get_context(payload: Login_PM):
    return UserController().login_user(payload)


@router.post("/no-check/signup")
async def signup(payload: SignUp_PM):
    return UserController().add_user(payload=payload)


@router.get("/validate-session")
async def validate_session():
    return JSONResponse(status_code=201, content="Successfully Validated the Json.")


@router.post("/logout")
async def logout_user():
    UserController().logout_user()
    return JSONResponse(status_code=201, content="Succefully Logged Out")
