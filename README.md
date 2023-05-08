# YaMDB API

### Описание проекта:

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся. Произведения делятся
на категории. Произведению может быть присвоен жанр из списка предустановленных. Добавлять произведения, категории и
жанры может только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (
целое число), из пользовательских оценок формируется усреднённая оценка произведения - рейтинг (целое число). На одно
произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только
аутентифицированные пользователи.

```
Ресурсы API YaMDb:
    auth: аутентификация.
    users: пользователи.
    titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
    categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
    genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
    reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
    comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
```

## Используется:

+ Python 3.7
+ Django 3.2
+ Django REST framework 3.12
+ Simple JWT
+ SQLite3

## Распаковка проекта

Развёртывание контейнеров в **Docker**:

```bash
# Переходим в папку проекта
cd ~/infra_sp2/infra
docker-compose up
# Создание миграций
docker-compose exec web python3 manage.py makemigrations
# Применение миграций
docker-compose exec web python3 manage.py migrate
# Создание суперпользователя
docker-compose exec web python3 manage.py createsuperuser
# Загрузка статики
docker-compose exec web python3 manage.py collectstatic --no-input
```

## Заполнение базы данных из CSV:

```
python manage.py csv_load
```

## Наполнение файла *.env*:

```
DB_ENGINE=движок БД (по умолчанию PostgreSQL)
DB_NAME=название БД 
POSTGRES_USER=пользователь БД 
POSTGRES_PASSWORD=пароль пользователя 
DB_HOST=контейнер с БД  
DB_PORT=порт для работы с бд
```

## Документация и эндпойнты:

[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Примеры запросов к API:

- GET: http://127.0.0.1:8000/api/v1/titles/1/

Request:

```J-SON
    "id": 1,
    "name": "Интерстеллар",
    "year": 2014,
    "description": null,
    "genre": [{"name": "Фантастика","slug": "fantastic"}],
    "category": {"name": "Фильм","slug": "movie"},
    "rating": 10
```

- GET: http://127.0.0.1:8000/api/v1/titles/1/reviews/1/

Request:

```J-SON
    "id": 1,
    "author": "Petrovich",
    "title": 1,
    "text": 
        "Обзор\отзыв в виде текста",
    "score": 10,
    "pub_date": "2023-02-23T00:00:01Z"
```

## Авторы:

###### Студенты курса "Python-разработчик" от Яндекс-Практикума

+ [Aster111](https://github.com/Aster111)
+ [Vas1levs47](https://github.com/Vas1levs47)

```text
Модели, View и эндпойнты для:
произведений,
категорий,
жанров,
отзывов,
комментариев,
рейтинга произведений
импорт данных из csv файлов
```

+ [Dzheronimo](https://github.com/dzheronimo)

```text
система регистрации и аутентификации,
права доступа,
работа с токеном,
система подтверждения через e-mail
```