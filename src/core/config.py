from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    films_api_base_url: str = Field(
        validation_alias='PROJECT_NAME', default='http://127.0.0.1:81/api/v1/'
    )


settings = Settings()
