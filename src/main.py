import uvicorn

from fastapi import FastAPI

from core.logger import LOGGING
from api.v1 import voice

app = FastAPI(
    title='Голосовой помощник',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    description="Голосовой пощник для получения различной информации о фильмах и участников",
    version="1.0.0",
)

app.include_router(voice.router, prefix='/api/v1/voice', tags=['voice'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING
    )
