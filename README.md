# idp_hacaton
Сервис для создания и отслеживания ИПР сотрудников. Разработка в рамках проекта Хакатон+.

## Авторы backend
* [Халёса Максим](https://github.com/makskhaliosa)
* [Алексей Чижов](https://github.com/chizhovsky)
* [Андрей Варачев](https://github.com/Dartanyun)
* [Рашид Аюпов](https://github.com/Rashid-creator-droid)

## Команда проекта

* Product manager – Леонид Богачук (@LeonidBogachuk)
* Project manager – Тарабуткина Юлиана (@Juliana_jull)
* Системный аналитик (Lead) – Сканави Павел (@Reds_on_tour)
* Системный аналитик – Андиева Диана (@keller_diana)
* Бизнес-аналитик (Lead) - Фадеева Алина (@Alina_a_Fadeeva)
* Бизнес-аналитик – Уразметова Лилия (@Lili_9092)
* Дизайнер (Lead) – Лапкина Яна (@yana_lapkina)
* Дизайнер – Лукинова Марина (@Lukinova_Marina)
* Дизайнер – Ерёменко Татьяна (@paintings_inspire)
* Backend (Lead) – Халёса Максим (@makskhaliosa)
* backend – Чижов Алексей (@Chizhovsky)
* backend – Варачев Андрей (@Dartanyun)
* backend – Рашид Аюпов (@valentaine_ra)
* frontend (Lead) – Красинский Роман (@r_krasinski)
* frontend – Сердюков Владислав (@VladisSerd)
* frontend – Мурадов Артур (@arturasterol)

## Документация проекта (Swagger)

http://51.250.70.185:8000/swagger/

## Сборка проекта

> [!NOTE]
> Проект можно запустить с планировщиком задачи и без него. См. ниже.

<details>

<summary>Запуск в докере</summary>

1. В корневой директории создать файл .env по примеру .env-sample.
* HOST - название контейнера с базой данных PostgresQL.
* Если проект запускается с планировщиком задач, то указать INCLUDE_CELERY=True, CELERY_BROKER_URL ('redis://localhost:6379/0') - вместо localhost указать название контейнера с Redis. То же самое для CELERY_RESULT_BACKEND.

#### Запуск с планировщиком задач (будут создаваться предупреждения о приближающихся сроках окончания задач и ИПР).

2. В корневой директории выполнить команду

```bash
sudo docker compose -f docker-compose-celery.yml up -d

sudo docker exec idp_hacaton-backend-1 python manage.py migrate
```

#### Без планировщика задач.

2. В корневой директории выполнить команду

```bash
docker compose up -d

sudo docker exec idp_hacaton-backend-1 python manage.py migrate
```
</details>

<details>

<summary>Запуск без докера</summary>

* Смотрите раздел "Детали для разработки" (Добавлен планировщик задач django-celery-beat)
</details>

## Стэк
* Django 5.0.1
* Django Rest Framework
* PostgresQL
* Django-celery-beat
* Redis
* Swagger

## Сторонние библиотеки
- [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [Djoser](https://github.com/sunscrapers/djoser)
- [Django-filters](https://django-filter.readthedocs.io/en/latest/index.html)
- [Drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [DRF-Simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)
- [Django-celery-beat](https://django-celery-beat.readthedocs.io/en/latest/index.html)

### Реализовано
* Работа с пользователями, авторизация пользователей по JWT токену.
* Работа с ИПР и Задачами, создание, обновление, удаление.
* Возможность запросить список ИПР авторизованного пользователя, список ИПР сотрудников авторизованного пользователя, список задач ИПР.
* Автоматическое создание объектов уведомлений в базе при создании и изменении объектов ИПР и Задач.
* Создание фоновых задач для смены статусов и создания уведомлений при наступлении временного дэдлайна.
* Возможность загружать файлы к задаче и скачивать файлы, прикрепленные к задаче.
* Возможность скачать сведения об ИПР сотрудников в формате Excel.
* Фильтрация и сортировка объектов Пользователи, ИПР и Задачи.
* Создание автодокументации.
* Добавлены объекты в админку Джанго, кастомизированы представления уведомлений в объектах ИПР и Задач, кастомизирована форма пользователей.

<details>

<summary>Детали при разработке</summary>

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
docker compose -f docker-compose-dbs up -d
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
1. Запустить базу
```bash
docker compose -f docker-compose-dbs.yml up -d
```
2. Выполнить миграции
```bash
python manage.py migrate
```
3. Запустить селери воркера
```bash
celery -A idp worker --loglevel=info -P eventlet
```
4. Запустить селери планировщика
```bash
celery -A idp beat -l info
```
5. Запустить проект
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
</details>
