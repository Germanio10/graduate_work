from contextlib import asynccontextmanager

import aiohttp
import uvicorn
from api.v1 import assistant
from core.config import settings
from db import abstract_repository, api_client
from db.remote_repository import RemoteRepository
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_client.session = aiohttp.ClientSession()
    client = api_client.ApiClient(base_url=settings.films_api_base_url, session=api_client.session)
    abstract_repository.db = RemoteRepository(api_client=client)

    yield

    await api_client.session.close()


app = FastAPI(
    title='settings.project_nam',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    # debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(assistant.assistant_route, prefix='/api/v1/assistant', tags=['assistant'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
