from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException
from models.response_model import ResponseAssitant
from models.user_question import UserQuestion
from service.handler_service import HandlerService, get_handler_service
from starlette import status
from starlette.requests import Request
from utils.check_auth import CheckAuth, get_check_auth_service

assistant_route = APIRouter()


@assistant_route.post(
    '/',
    description='Вопрос пользователя',
    status_code=HTTPStatus.CREATED,
    response_model=ResponseAssitant,
)
async def search(
    request: Request,
    question: UserQuestion = Body(),
    service: HandlerService = Depends(get_handler_service),
    check_auth: CheckAuth = Depends(get_check_auth_service),
):
    user = await check_auth.check_authorization(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please login')
    message = await service.execute(question=question, user_id=user.user_id)
    return ResponseAssitant(answer=message)
