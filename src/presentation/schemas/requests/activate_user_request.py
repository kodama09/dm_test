from pydantic import BaseModel, Field


class ActivateUserRequest(BaseModel):
    activation_code: str = Field(min_length=4, max_length=12)
