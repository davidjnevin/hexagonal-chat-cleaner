from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from chatcleaner.adapters.db.orm import start_mappers
from chatcleaner.adapters.entrypoints.api.base import api_router
from chatcleaner.configurator.containers import Container


def include_router(app_):
    app_.include_router(api_router)


def configure_cors(app_):
    origins = [
        "*",
        "http://localhost:5173",  # Allow only front end - local development
        "https://hexagonalchat.netlify.app/",  # Allow only front end - prod
        "https://netlify--hexagonalchat.netlify.app",  # Allow only front end
    ]
    # Allow these methods to be used
    methods = ["OPTIONS", "GET", "POST", "PUT"]
    headers = ["*"]

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=methods,
        allow_headers=headers,
    )


def start_application():
    container = Container()
    app_ = FastAPI(title="Chat Cleaner")
    app_.container = container
    include_router(app_)
    configure_cors(app_)

    # start orm mappers
    try:
        start_mappers()
    except Exception as err:
        if "already has a primary mapper defined" not in str(err):
            raise RuntimeError(err) from err
    return app_


app = start_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
