from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from models.response_model import ResponseAssitant
from models.user_question import UserQuestion
from service.handler_service import HandlerService, get_handler_service

assistant_route = APIRouter()


@assistant_route.post(
    '/',
    description='Вопрос пользователя',
    status_code=HTTPStatus.CREATED,
    response_model=ResponseAssitant,
)
async def search(
    question: UserQuestion = Body(), service: HandlerService = Depends(get_handler_service)
):
    message = await service.execute(question)
    print(message)
    return ResponseAssitant(answer=message)
