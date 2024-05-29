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
        ('Сколько фильмов снял Джонни Дэп',
         "Джонни Дэп снял 2 фильма: Гладиатор, Гарри Поттер и философский камень",
         status.HTTP_201_CREATED),
        ('В каких фильмах играл Джонни Деп',
         "актер Джонни Деп снимался в фильмах: Спасти рядового Райана, В погоне за счастьем, Терминатор 2: Судный день",
         status.HTTP_201_CREATED),
        ('неизвестный фильм',
         'Извините но мы можем подскзать только о нашей коллеции фильмов',
         status.HTTP_201_CREATED)
    ]
)
async def test_api(make_post_request, text, answer, expected_status):
    data = {"text": text}
    response = await make_post_request(data=data, method='assistant/')

    assert response['status'] == expected_status
    assert response['body'].get('answer') == answer
