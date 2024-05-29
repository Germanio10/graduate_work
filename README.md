# Проектная работа: диплом

## .env файл
Для настройки переменных среды нужно скопировать пример конфигурации [.env.example](.env.example)
```sh
cp .env.example .env
```

## Запуск проекта
Для запуска проекта необходимо ввести команду
```shell
docker compose up
```

## Запуск распознавания и синтеза речи
Для запуска необходимо:

Создать виртуальное окружение и активировать его:
```shell
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```
Установить зависимости:
```shell
pip install -r requirements.txt
```
Ввести команду:
```shell
python assistant_client/src/main.py
```

# Переменные окружения, используемые в проекте

- [DEBUG](#DEBUG)
- [PROJECT_NAME](#PROJECT_NAME)
- [PROJECT_URL](#PROJECT_URL)
- [DB_NAME](#DB_NAME)
- [DB_USER](#DB_USER)
- [DB_PASSWORD](#DB_PASSWORD)
- [DB_HOST](#DB_HOST)
- [DB_PORT](#DB_PORT)
- [PARSE_SIZE](#PARSE_SIZE)
- [UPDATED_DAYS_LIMIT](#UPDATED_DAYS_LIMIT)
- [RERUN](#RERUN)
- [ELASTICSEARCH_URL](#ELASTICSEARCH_URL)
- [ELASTICSEARCH_LOAD_SIZE](#ELASTICSEARCH_LOAD_SIZE)
- [ELASTIC_HOST](#ELASTIC_HOST)
- [ELASTIC_PORT](#ELASTIC_PORT)
- [ELASTIC_LOAD_SIZE](#ELASTIC_LOAD_SIZE)
- [REDIS_HOST](#REDIS_HOST)
- [REDIS_PORT](#REDIS_PORT)
- [YANDEX_TOKEN](#YANDEX_TOKEN)
- [YANDEX_CATALOG](#YANDEX_CATALOG)

## <p id="DEBUG">DEBUG</p>
Режим отладки (True/False).

## <p id="PROJECT_NAME">PROJECT_NAME</p>
Название проекта.

## <p id="PROJECT_URL">PROJECT_URL</p>
URL проекта.

## <p id="DB_NAME">DB_NAME</p>
Имя базы данных PostgreSQL.

## <p id="DB_USER">DB_USER</p>
Пользователь базы данных PostgreSQL.

## <p id="DB_PASSWORD">DB_PASSWORD</p>
Пароль к базе данных PostgreSQL.

## <p id="DB_HOST">DB_HOST</p>
Хост базы данных PostgreSQL.

## <p id="DB_PORT">DB_PORT</p>
Порт базы данных PostgreSQL.

## <p id="PARSE_SIZE">PARSE_SIZE</p>
Размер парсинга данных.

## <p id="UPDATED_DAYS_LIMIT">UPDATED_DAYS_LIMIT</p>
Лимит дней для обновления данных.

## <p id="RERUN">RERUN</p>
Количество повторных запусков.

## <p id="ELASTICSEARCH_URL">ELASTICSEARCH_URL</p>
URL Elasticsearch.

## <p id="ELASTICSEARCH_LOAD_SIZE">ELASTICSEARCH_LOAD_SIZE</p>
Размер загрузки данных в Elasticsearch.

## <p id="ELASTIC_HOST">ELASTIC_HOST</p>
Хост Elasticsearch.

## <p id="ELASTIC_PORT">ELASTIC_PORT</p>
Порт Elasticsearch.

## <p id="ELASTIC_LOAD_SIZE">ELASTIC_LOAD_SIZE</p>
Размер загрузки данных в Elasticsearch.

## <p id="REDIS_HOST">REDIS_HOST</p>
Хост Redis.

## <p id="REDIS_PORT">REDIS_PORT</p>
Порт Redis.

## <p id="YANDEX_TOKEN">YANDEX_TOKEN</p>
Токен Яндекс для speechkit.

## <p id="YANDEX_CATALOG">YANDEX_CATALOG</p>
Каталог Яндекс для speechkit.
