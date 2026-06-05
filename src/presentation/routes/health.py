from fastapi import APIRouter

from src.config.metadata import load_application_metadata
from src.presentation.schemas.responses.health_response import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    metadata = load_application_metadata()

    return HealthResponse(
        name=metadata.name,
        version=metadata.version,
        codename=metadata.codename,
        status="ok",
    )
