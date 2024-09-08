# Описание «Фудграм»

«Фудграм» — сайт, на котором пользователи будут публиковать свои рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других
авторов. Зарегистрированным пользователям также будет доступен сервис
«Список покупок». Он позволит создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.


### Технологический стек 
- Python 3.9  
- Django  
- Django Rest Framework
- React
- Postgresql
- NGINX
- Docker
- gunicorn
- GitHub Actions


### Функционал проекта
Публикация рецептов: зарегистрированные пользователи могут создавать рецепты, добавляя описание, изображение, ингредиенты и этапы приготовления.
Избранное: возможность добавлять рецепты в избранное для быстрого доступа к ним в будущем.
Список покупок: создание списка покупок из выбранных рецептов. Список можно скачать в виде текстового файла.
Подписка на авторов: пользователи могут подписываться на других авторов и следить за их новыми публикациями.
Фильтрация и поиск: фильтрация рецептов по тегам и возможность поиска по названию.


# Установка и запуск (Windows)
### Клонировать репозиторий и перейти в него в командной строке:
```
$ git clone https://github.com/Mikavak/foodgram.git
$ cd foodgram
```

### Cоздать и активировать виртуальное окружение:
```
$ py -m venv venv
$ source venv/bin/activate
```

### Установить зависимости:
```
$ py -m pip install --upgrade pip
$ pip install -r requirements.txt
```

## Запуск Docker:
### Соберите и запустите контейнеры
```
$ docker-compose up -d --build
```

### Выполните миграции для базы данных:
```
$ docker compose exec backend python manage.py migrate
```

### Создайте суперпользователя для доступа в админку:
```
$ docker compose exec backend python manage.py createsuperuser
```

### Соберите статику:
```
$ docker compose exec backend python manage.py collectstatic --noinput

```

### Заполните ингредиенты:
```
$ docker compose exec backend python manage.py import_csv ingredients.csv
```

## Развертывание на сервере
- Установите Docker и Docker Compose на сервер.
- Скопируйте файлы проекта на сервер.
- Запустите проект командой:
```
docker-compose up --build -d
```

# Примеры запросов:

#### GET /api/recipes/ — получение списка рецептов

#### POST /api/recipes/ — добавление нового рецепта
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAA
  BieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACkl
  EQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```

#### GET /api/recipes/{id}/ — получение рецепта по ID.

#### POST /api/recipes/{id}/favorite/ — добавление рецепта в избранное.

#### POST /api/recipes/{id}/shopping_cart/ - добавление рецепта в список покупок. 

# Сервисы и архитектура

## Проект состоит из следующих контейнеров:

- db — база данных PostgreSQL
- backend — Django-приложение (API).
- frontend — React-приложение (интерфейс).
- nginx — прокси-сервер для управления запросами.


### Авторы
####   [Авакумов Михаил](https://github.com/Mikavak)