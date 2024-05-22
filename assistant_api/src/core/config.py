from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str = Field(validation_alias='REDIT_HOST', default='127.0.0.1')
    port: int = Field(validation_alias='REDIS_PORT', default=6379)


class Settings(BaseSettings):
    project_name: str = Field(validation_alias='PROJECT_NAME', default='assistent')
    films_api_base_url: str = Field(
        validation_alias='PROJECT_NAME', default='http://127.0.0.1:81/api/v1/'
    )
    redis_settings: RedisSettings = RedisSettings()


settings = Settings()
