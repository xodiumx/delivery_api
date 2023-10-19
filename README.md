# Delivery api

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-000000?style=for-the-badge&logo=django&logoColor=white&color=3F888F&labelColor=black) ![Swagger](https://img.shields.io/badge/swagger-000000?style=for-the-badge&logo=python&logoColor=white) ![PEP8](https://img.shields.io/badge/pep8-000000?style=for-the-badge&logo=python&logoColor=white) ![Celery](https://img.shields.io/badge/celery-3F888F?style=for-the-badge&logo=python&logoColor=white) ![Redis](https://img.shields.io/badge/redis-3F888F?style=for-the-badge&logo=redis&logoColor=white) ![Postgres](https://img.shields.io/badge/postgresql-3F888F?style=for-the-badge&logo=postgresql&logoColor=white)

## Задание

Необходимо реализовать *API* сервис, который поддерживает следующие функции:
- Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
- Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза (=< 450 миль));
- Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
- Редактирование машины по ID (локация (определяется по введенному zip-коду));
- Редактирование груза по ID (вес, описание);
- Удаление груза по ID.
- Фильтр списка грузов (вес, мили ближайших машин до грузов);
- Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную).

### Структура БД

Груз обязательно должен содержать следующие характеристики:
- локация pick-up;
- локация delivery;
- вес (1-1000);
- описание.

Машина обязательно должна в себя включать следующие характеристики:
- уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце, пример: "1234A", "2534B", "9999Z")
- текущая локация;
- грузоподъемность (1-1000).

Локация должна содержать в себе следующие характеристики:
- город;
- штат;
- почтовый индекс (zip);
- широта;
- долгота.

## Доступные endpoint-ы
```
api/v1/cargoes/ (POST)
api/v1/cargoes/ (GET)
api/v1/cargoes/{id}/ (GET)
api/v1/cargoes/{id}/ (PATCH)
api/v1/cargoes/{id}/ (DELETE)

api/v1/cars/{id}/ {PATCH}
```

## Пример запросов и ответов API
- POST - запрос на endpont `api/v1/cargoes/`, создание объекта груза, поля: `pick_up` и `delivery_to` принимают zip-индексы.
```
{
  "pick_up": "00601",
  "delivery_to": "00602",
  "weight": 600,
  "description": "600 kg of cookies"
}
```
Ответ:
```
{
  "pick_up": "Adjuntas Puerto Rico 00601",
  "delivery_to": "Aguada Puerto Rico 00602",
  "weight": 600,
  "description": "600 kg of cookies"
}
```
- PATCH - запрос на `api/v1/cargoes/{id}/`, обновление полей (вес и описание) груза.
```
{
  "weight": 1000,
  "description": "mistake, 1000 kg of cookies"
}
```
Ответ:
```
{
  "pick_up": "Adjuntas Puerto Rico 00601",
  "delivery_to": "Aguada Puerto Rico 00602",
  "weight": 1000,
  "description": "mistake, 1000 kg of cookies"
}
```
- Для автоматического обновления локаций у всех автомобилей, раз в 3 минуты запускается `celery task`, которая находится в приложении `api`

#### Подробная документация по endpoint-y `swagger/`

## Для загрузки и удаления `uszips.csv` созданы команды:
- Загрузка:
```
python manage.py import_data --load
```
- Удаление
```
python manage.py import_data --delete
```

## Установка проекта через `docker`

1. клонируйте репозиторий:
```
git clone git@github.com:xodiumx/test_for_welbex.git
```
2. Перейдите в директорию `infra`
```
cd infra
```
3. В этой директории создайте файл `.env` пример:
```
SECRET_KEY='django-insecure-_if(yed4o4u9j!vm(rq*yq^yqcvj*)wxzg*6l_gbqjh&om=8x4'

DB_ENGINE=django.db.backends.postgresql
DB_NAME=delivery
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
DB_HOST=db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_TASK_TRACK_STARTED=True
CELERY_TASK_TIME_LIMIT=60
```
4. Выполните команду:
```
docker-compose up -d
```
5. В контейнере `db` выполните команды:
```
psql -U postgres
CREATE DATABASE delivery;
```
6. В контейнере `back` выполните команду:
```
python3 manage.py makemigrations --force-color -v 3 \
&& python3 manage.py migrate --force-color -v 3 \
&& python3 manage.py collectstatic \
&& python3 manage.py loaddata fixtures.json
```
- superuser - `admin:admin`
