from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db

from app.routes.web import router as web_router
from app.routes.api import router as api_router
from app.routes.auth import router as auth_router


def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description=(
            "Budget-aware AI recommendation assistant "
            "for Home, Party and Jewelry planning."
        ),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount(
        "/static",
        StaticFiles(directory="app/static"),
        name="static"
    )

    app.include_router(web_router)
    app.include_router(auth_router)
    app.include_router(api_router)

    return app


app = create_app()


@app.on_event("startup")
def startup():
    init_db()