from pathlib import Path

from pydantic import SecretStr
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parent.parent.resolve() / ".env"


class PostgreSQLSettings(BaseSettings):
    mode: str
    database_name: str
    driver: str
    user: str
    password: SecretStr
    host: str
    port: int

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+{self.driver}://{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.database_name}"
        )

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", env_prefix="DB_"
    )


class AuthSettings(BaseSettings):
    jwt_secret: SecretStr
    jwt_algorithm: str
    access_token_expire: int
    refresh_token_expire: int

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", env_prefix="AUTH_"
    )


class RedisSettings(BaseSettings):
    database_name: str | int
    user: str | None = None
    password: SecretStr | None = None
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", env_prefix="REDIS_"
    )


class Settings(BaseSettings):
    database: PostgreSQLSettings = Field(default_factory=PostgreSQLSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)


settings = Settings()
