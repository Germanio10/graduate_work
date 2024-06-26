from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class YandexTokenSettings(BaseSettings):
    token: str = Field(alias='YANDEX_TOKEN')
    catalog: str = Field(alias='YANDEX_CATALOG')
    project_url: str = Field(alias='PROJECT_URL')


class Settings(BaseSettings):
    yandex_settings: YandexTokenSettings = YandexTokenSettings()


settings = Settings()
