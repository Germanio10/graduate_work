import logging

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

CACHE_EXPIRE_IN_SECONDS = 30
NER_MODEL_PATH = 'nlp_models/model-best'
CLASSIFICATOR_MODEL_PATH = 'nlp_models/classificator.pth'
INTENTS_PATH = 'nlp_models/current_intents.json'

NO_CONTENT = 'Извините но не хватает контекста. Вы можете спросить о фильме в нашей коллекции режиссере актере'
NO_FILM_IN_BASE = 'Извините но такого фильма у нас нет'
NO_INTENTS = 'Извините но мы можем подскзать только о нашей коллеции фильмов'
NO_INFO_FILM = 'Извините но у нас нет такой информации по данному фильму'
NOT_FOUND = 'Прошу прощения но ничего не найдено. Вы можете спросить о фильме в нашей коллекции режиссере актере'


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
    match_percent: float = Field(validation_alias='MATCH_PERCENT', default=0.85)


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False


settings = Settings()
