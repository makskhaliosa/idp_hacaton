# idp_hacaton
Сервис для создания и отслеживания ИПР сотрудников. Разработка в рамках проекта Хакатон+.

## Настроен pre-commit
Обязательно установить pre-commit
```bash
pre-commit install
```

В первый раз можно прогнать все файлы для проверки
```bash
pre-commit run --all-files
```
После этого перед каждым коммитом будет автоматическая проверка кода на ошибки.

## Добавлен файл .env
Создать файл по примеру .env-sample

## Добавлено подключение к БД PostgresQL
Для подключения к базе можно запустить Postgres в докере
```bash
docker compose -f docker-compose-postgres up -d
```

Либо запустить Postgres локально и создать базу там.


## Добавлена возможность загрузки данных из фикстур.

Фикстуры располагаются в папках приложения в подкаталоге /fixtures.
Для активации фикстур необходимо прописать команду:
```bash
python manage.py loaddata */fixtures/*.json
```

Также из фикстур создается базовая admin запись со следующими данными.

email: admin@admin.ru
password: admin


## Добавлен планировщик задач django-celery-beat

Нужно обновить файл с переменными .env

Из-за того что django-celery-beat автоматически устанавливает Django==4.2.9, нужно после установки зависимостей отдельно установить Django==5.0.1

Для запуска локально сначала нужно сделать все миграции.
Для запуска в докере нужно будет сделать миграции из контейнера backend.

Локально потребуется три консоли
1.
```bash
celery -A idp worker --loglevel=info -P eventlet
```
2.
```bash
celery -A idp beat -l info
```
3.
```bash
python manage.py runserver
```

Для запуска докера с планировщиком

```bash
docker compose -f docker-compose-celery.yml up -d
```

Без планировщика обычный докер компоуз
```bash
docker compose up
```
