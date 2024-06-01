from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(f"{BASE_DIR}/.env")


class TestAssistantServiceSettings(BaseSettings):
    host: str = Field(validation_alias='ASSISTANT_HOST', default='localhost')
    port: int = Field(validation_alias='ASSISTANT_PORT', default='8000')

    def url(self):
        return f'http://{self.host}:{self.port}/api/v1'


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"


class TestSettings(BaseSettings):
    assistant_service: TestAssistantServiceSettings = TestAssistantServiceSettings()


test_settings = TestSettings()
