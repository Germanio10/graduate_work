import pytest
from starlette import status


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ('text', 'answer', 'expected_status'),
    [
        (
            'какой рейтинг фильма гладиатор',
            'рейтинг фильма гладиатор составляет 8.5',
            status.HTTP_201_CREATED
        ),
        ('кто его снял',
        'режиссер фильма гладиатор был Джонни Депп',
        status.HTTP_201_CREATED),
        ('какой жанр фильма гладиатор',
         'жанры фильма гладиатор Драма',
         status.HTTP_201_CREATED),
        ('Сколько фильмов снял Джонни Депп',
         "Джонни Депп снял 2 фильма: Гладиатор, Гарри Поттер и философский камень",
         status.HTTP_201_CREATED),
        ('В каких фильмах снимался Джонни Депп',
         "актер Джонни Депп снимался в фильмах: Спасти рядового Райана, В погоне за счастьем, Терминатор 2: Судный день",
         status.HTTP_201_CREATED),
        ('неизвестный фильм',
         'Извините но не хватает контекста. Вы можете спросить о фильме в нашей коллекции режиссере актере',
         status.HTTP_201_CREATED)
    ]
)
async def test_api(make_post_request,  get_token, text, answer, expected_status):
    data = {"text": text}
    access_token = await get_token()
    response = await make_post_request(data=data, method='assistant/', access_token=access_token)

    assert response['status'] == expected_status
    assert response['body'].get('answer') == answer
