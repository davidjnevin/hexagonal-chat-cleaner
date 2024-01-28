from fastapi import FastAPI

from chatcleaner.adapters.db.orm import start_mappers
from chatcleaner.adapters.entrypoints.api.base import api_router
from chatcleaner.configurator.containers import Container


def include_router(app_):
    app_.include_router(api_router)


def start_application():
    container = Container()
    app_ = FastAPI(title="Chat Cleaner")
    app_.container = container
    include_router(app_)
    # start orm mappers
    try:
        start_mappers()
    except Exception as err:
        if "already has a primary mapper defined" not in str(err):
            raise RuntimeError(err) from err
    return app_


app = start_application()
