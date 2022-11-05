# api_yamdb

О проекте: YaMDb собирает отзывы пользователей на различные произведения. 
Вы можете добавить отзыв к произведению только один раз, а также комментарий к этому отзыву.
Авторы: Толстопятов Владимир, Яппаров Рустам, Марковская Татьяна


### Как запустить проект:

Шаблон env-файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
LANG=en_US.utf8
```
Перейти в папку с файлом docker-compose:
```
cd infra
```
Запуск docker-compose:
```
docker-compose up -d --build
```
Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```
Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Заполнить базу данных:
```
python manage.py loaddata fixtures.json
```
