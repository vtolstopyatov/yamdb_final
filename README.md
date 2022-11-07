![example workflow](https://github.com/vtolstopyatov/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
# api_yamdb

О проекте: YaMDb собирает отзывы пользователей на различные произведения. 
Вы можете добавить отзыв к произведению только один раз, а также комментарий к этому отзыву.
Авторы: Толстопятов Владимир, Яппаров Рустам, Марковская Татьяна

Проект запущен и доступен по адресу http://51.250.2.92/redoc/

### Как запустить проект на сервере:

- Перейти в папку с файлом docker-compose:
```
cd infra
```
- Запуск docker-compose:
```
docker-compose up -d --build
```
- Выполнить миграции:
```
docker-compose exec web python manage.py migrate
```
- Собрать статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
- На сервере остановите службу nginx:
```
sudo systemctl stop nginx
```
- Добавьте переменные окружения для GitHub Action:
```
Settings → Secrets → Actions → New repository secret
```
- После фиксации и отправки изменений в ветку main — проект запустится на сервере
