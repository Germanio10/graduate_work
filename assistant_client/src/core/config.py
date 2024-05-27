from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class YandexTokenSettings(BaseSettings):
    token: str = Field(alias='YANDEX_TOKEN')
    catalog: str = Field(alias='YANDEX_CATALOG')


class Settings(BaseSettings):
    yandex_settings: YandexTokenSettings = YandexTokenSettings()


settings = Settings()
