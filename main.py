from typing import cast
from fastapi import FastAPI
from decouple import config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.enums.MiscEnums import ServicePaths
from app.middlewares.rest import ExceptionMiddleware, HeaderValidationMiddleware
from app.routers import Chat, User
from lifespans import Lifespans, mongodb_lifespan

app = FastAPI(
    title=ServicePaths.AI_SERVICE.value,
    description="A  Multi Agent Interaction Service .",
    version="0.0.2",
    lifespan=Lifespans(
        [
            mongodb_lifespan,
        ]
    ),
)

app.add_middleware(
    HeaderValidationMiddleware,
    x_api_key_1=cast(str, config("X_API_KEY_AIS_1")),
    x_api_key_2=cast(str, config("X_API_KEY_AIS_2")),
    excluded_paths=frozenset(
        [
            f"{ServicePaths.CONTEXT_PATH.value}/healthcheck",
            f"{ServicePaths.CONTEXT_PATH.value}/user/no-check/",
        ]
    ),
)

app.add_middleware(ExceptionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://app001-user-service.onrender.com",
        "https://aiassistly.com",
        "https://remarkable-conkies-27cbe1.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Chat.router)
app.include_router(User.router)


@app.get(ServicePaths.CONTEXT_PATH.value + "/healthcheck")
def health_check():
    return JSONResponse(status_code=200, content="Jai Mata Di .Working Fine. Yeah !")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=3090,
        host="0.0.0.0",
        reload=False,
        workers=1,
        lifespan="on",
    )
