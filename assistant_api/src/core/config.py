import logging

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

CACHE_EXPIRE_IN_SECONDS = 30


class RedisSettings(BaseSettings):
    host: str = Field(validation_alias='REDIT_HOST', default='127.0.0.1')
    port: int = Field(validation_alias='REDIS_PORT', default=6379)


class ElasticsearchSettings(BaseSettings):
    host: str = Field(validation_alias='ELASTIC_HOST', default='127.0.0.1')
    port: int = Field(validation_alias='ELASTIC_PORT', default=9200)

    def url(self):
        return f'http://{self.host}:{self.port}'


class Settings(BaseSettings):
    debug: bool = Field(validation_alias='DEBUG', default=True)
    project_name: str = Field(validation_alias='PROJECT_NAME', default='assistent')
    films_api_base_url: str = Field(
        validation_alias='MOVIES_API_BASE_URL', default='http://127.0.0.1:81/api/v1/'
    )
    redis_settings: RedisSettings = RedisSettings()
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()
    log_level: int | str = Field(validation_alias='LOG_LEVEL', default=logging.INFO)


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False


settings = Settings()
