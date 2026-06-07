import pytest

from src.config.metadata import load_application_metadata

pytestmark = [pytest.mark.anyio, pytest.mark.functional]


async def test_health_endpoint_returns_application_metadata(http_client) -> None:
    metadata = load_application_metadata()

    response = await http_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "name": metadata.name,
        "version": metadata.version,
        "codename": metadata.codename,
        "status": "ok",
    }
