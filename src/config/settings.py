from functools import lru_cache
from typing import Literal, Self
from urllib.parse import quote

from pydantic import PositiveFloat, PositiveInt, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    activation_code_secret: SecretStr = SecretStr("local_activation_code_secret")
    app_env: Literal["local", "test", "production"] = "local"
    postgres_db: str = "user_registration"
    postgres_host: str = "localhost"
    postgres_password: SecretStr = SecretStr("user_registration_password")
    postgres_port: int = 5432
    postgres_pool_command_timeout: PositiveFloat = 30.0
    postgres_pool_max_size: PositiveInt = 10
    postgres_pool_min_size: PositiveInt = 1
    postgres_user: str = "user_registration"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def postgres_dsn(self) -> str:
        user = quote(self.postgres_user, safe="")
        password = quote(self.postgres_password.get_secret_value(), safe="")
        database = quote(self.postgres_db, safe="")

        return (
            f"postgresql://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{database}"
        )

    @model_validator(mode="after")
    def validate_postgres_pool_sizes(self) -> Self:
        if self.postgres_pool_min_size > self.postgres_pool_max_size:
            msg = (
                "postgres_pool_min_size must be less than or equal to "
                "postgres_pool_max_size"
            )
            raise ValueError(msg)

        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
