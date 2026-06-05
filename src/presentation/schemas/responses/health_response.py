from pydantic import BaseModel


class HealthResponse(BaseModel):
    name: str
    version: str
    codename: str
    status: str
