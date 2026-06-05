from fastapi import FastAPI

from src.bootstrap.lifespan import lifespan
from src.config.metadata import load_application_metadata
from src.presentation.routes.health import router as health_router


def create_app() -> FastAPI:
    metadata = load_application_metadata()
    app = FastAPI(
        title=metadata.name,
        version=metadata.version,
        lifespan=lifespan,
    )
    app.include_router(health_router)

    return app
