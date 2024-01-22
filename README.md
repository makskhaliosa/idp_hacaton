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
`python manage.py loaddata */fixtures/*.json`
