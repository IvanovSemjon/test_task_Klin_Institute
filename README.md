# Система учёта работников компании

[![CI](https://github.com/username/hr-workers/actions/workflows/ci.yml/badge.svg)](https://github.com/username/hr-workers/actions/workflows/ci.yml)
[![Docker Build](https://github.com/username/hr-workers/actions/workflows/docker.yml/badge.svg)](https://github.com/username/hr-workers/actions/workflows/docker.yml)
[![Code Quality](https://github.com/username/hr-workers/actions/workflows/code-quality.yml/badge.svg)](https://github.com/username/hr-workers/actions/workflows/code-quality.yml)

REST API система для управления сотрудниками компании с Django Admin панелью.

## Технический стек

- **Backend**: Python 3.13+ | Django 4.2+ (LTS) | Django REST Framework
- **База данных**: PostgreSQL 15
- **Управление зависимостями**: Poetry
- **Контейнеризация**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Тестирование**: pytest-django
- **Качество кода**: Black, isort

## Функциональность

### Модель Worker
- **first_name** — имя (обязательное)
- **middle_name** — отчество (необязательное)
- **last_name** — фамилия (обязательное)
- **email** — email (уникальный, обязательный)
- **position** — должность (обязательное)
- **is_active** — активен ли работник (по умолчанию True)
- **hired_date** — дата приёма на работу (автоматически)
- **created_by** — пользователь, создавший запись
- **created_at, updated_at** — технические поля для аудита
- **is_deleted** — мягкое удаление

### REST API Endpoints
- `GET /api/workers/` — список работников (с пагинацией)
- `POST /api/workers/` — создание работника
- `GET /api/workers/{id}/` — детальная информация
- `PATCH /api/workers/{id}/` — обновление
- `DELETE /api/workers/{id}/` — удаление (мягкое)
- `POST /api/workers/import/` — импорт из Excel

### Особенности API
- **Пагинация**: 10 записей на страницу
- **Фильтрация**: по `is_active` и `position`
- **Права доступа**: 
  - Неавторизованные пользователи — только чтение
  - Admin/Staff — полный доступ (CRUD)
- **Разные сериализаторы**: упрощенный для списка, полный для деталей

## Быстрый старт

### 🐳 Запуск с Docker (рекомендуется)

```bash
# Клонирование репозитория
git clone <repository-url>
cd hr_workers_project

# Запуск всех сервисов
docker compose up --build
```

Приложение будет доступно на:
- **API**: http://localhost:8000/api/workers/
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/

### 🔧 Локальная разработка

#### 1. Установка зависимостей
```bash
git clone <repository-url>
cd hr_workers_project
poetry install
```

#### 2. Настройка PostgreSQL
```bash
# Установите PostgreSQL и создайте БД
createdb -U postgres hr_workers_db
```

#### 3. Настройка переменных окружения
Создайте файл `.env`:
```env
# Database
DB_NAME=hr_workers_db
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
```

#### 4. Запуск приложения
```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

## Создание пользователей с разными ролями

### Через Django Admin
1. Перейдите в админку: http://127.0.0.1:8000/admin/
2. Войдите под суперпользователем
3. Создайте пользователей в разделе "Users"

### Через Django Shell
```bash
poetry run python manage.py shell
```

```python
from django.contrib.auth.models import User

# Обычный пользователь (только чтение API)
user = User.objects.create_user(
    username='regular_user',
    email='user@example.com',
    password='userpass123'
)

# Администратор (полный доступ к API)
admin = User.objects.create_user(
    username='admin_user',
    email='admin@example.com',
    password='adminpass123',
    is_staff=True
)
```

### Роли и права доступа
- **Неавторизованные пользователи**: только GET запросы к API
- **Обычные пользователи**: только GET запросы к API
- **Staff пользователи**: полный CRUD доступ к API и админке

## Запуск тестов

```bash
# Запуск всех тестов
poetry run python manage.py test

# Запуск тестов с подробным выводом
poetry run python manage.py test --verbosity=2

# Запуск конкретного теста
poetry run python manage.py test workers.tests.WorkerAPITest.test_create_worker_as_admin
```

### Покрытие тестами (13 тестов)
- ✅ **Модель Worker**: создание, валидация, строковое представление
- ✅ **API endpoints**: все CRUD операции
- ✅ **Права доступа**: разные роли пользователей
- ✅ **Фильтрация**: по `is_active` и `position`
- ✅ **Импорт Excel**: успешный импорт и обработка ошибок
- ✅ **Мягкое удаление**: проверка корректной работы
- ✅ **Пагинация**: проверка работы с большими данными

```bash
# Запуск всех тестов
poetry run python manage.py test --verbosity=2

# Запуск конкретного теста
poetry run python manage.py test workers.tests.WorkerAPITest.test_create_worker_as_admin
```

## Тестирование импорта данных

### 1. Подготовка Excel файла
Используйте шаблон `import_template.xlsx` или создайте файл со столбцами:
- `first_name` — имя
- `middle_name` — отчество (может быть пустым)
- `last_name` — фамилия
- `email` — email
- `position` — должность
- `is_active` — TRUE/FALSE

### 2. Импорт через API
```bash
curl -X POST http://127.0.0.1:8000/api/workers/import/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@import_template.xlsx"
```

### 3. Импорт через DRF Browsable API
1. Перейдите на http://127.0.0.1:8000/api/workers/import/
2. Авторизуйтесь как staff пользователь
3. Загрузите Excel файл через форму

### 4. Ответ API
```json
{
  "Создан": 10,
  "Ошибки": [
    "Строка 5: отсутствуют обязательные поля",
    "Строка 7: Ошибка: UNIQUE constraint failed"
  ]
}
```

## Использование API

### Примеры запросов

```bash
# Получить список работников
GET /api/workers/

# Фильтрация по активности
GET /api/workers/?is_active=true

# Фильтрация по должности
GET /api/workers/?position=Разработчик

# Пагинация
GET /api/workers/?page=2

# Создание работника (требует авторизации как staff)
POST /api/workers/
{
  "first_name": "Иван",
  "last_name": "Петров",
  "email": "ivan@example.com",
  "position": "Разработчик"
}

# Обновление работника
PATCH /api/workers/1/
{
  "position": "Старший разработчик"
}
```

## Django Admin

Админка доступна по адресу: http://127.0.0.1:8000/admin/

### Возможности админки:
- **Фильтры**: по активности, должности, дате приема
- **Поиск**: по имени, фамилии, email, должности
- **Редактирование в списке**: is_active, position
- **Полная информация**: все поля модели
- **Логирование**: автоматическое в консоль при создании

## Структура проекта

```
hr_workers_project/
├── .github/workflows/      # GitHub Actions
│   ├── ci.yml             # CI Pipeline
│   ├── docker.yml         # Docker Build
│   └── code-quality.yml   # Code Quality
├── config/                 # Настройки Django
│   ├── settings.py        # Основные настройки
│   ├── urls.py            # URL маршруты
│   └── wsgi.py            # WSGI приложение
├── workers/                # Приложение работников
│   ├── models.py          # Модель Worker
│   ├── serializers.py     # DRF сериализаторы
│   ├── views.py           # API ViewSet
│   ├── admin.py           # Django Admin
│   ├── urls.py            # URL маршруты
│   └── tests.py           # Тесты (13 тестов)
├── docker-compose.yml      # Docker Compose
├── Dockerfile             # Docker образ
├── pyproject.toml         # Poetry зависимости
├── .env                   # Переменные окружения
├── .gitignore            # Git исключения
├── .dockerignore         # Docker исключения
└── import_template.xlsx   # Шаблон для импорта
```

## Docker команды

```bash
# Запуск в фоне
docker compose up -d

# Просмотр логов
docker compose logs -f web

# Выполнение команд в контейнере
docker compose exec web poetry run python manage.py shell

# Остановка и удаление
docker compose down -v

# Пересборка образов
docker compose build --no-cache
```

## Особенности реализации

### Архитектура
- **Мягкое удаление**: записи помечаются как удаленные (`is_deleted=True`)
- **Аудит**: автоматическое отслеживание `created_at`, `updated_at`
- **Логирование**: вывод в консоль при создании работников
- **Валидация**: проверка обязательных полей и уникальности email
- **Индексы**: оптимизация запросов по `email`, `position`, `is_active`

### Безопасность
- Переменные окружения для секретных данных
- Валидация прав доступа (IsAdminOrReadOnly)
- CSRF защита
- SQL injection защита через ORM

### Производительность
- Пагинация API (10 записей на страницу)
- Индексы базы данных
- `select_related` для оптимизации запросов
- Кэширование зависимостей в CI

### Мониторинг и отладка
- Подробные логи импорта Excel
- Отчеты об ошибках с указанием строк
- Health checks для Docker
- Автоматические тесты покрывают всю функциональность

## CI/CD и автоматизация

### GitHub Actions
Проект включает 3 workflow:

1. **CI Pipeline** (`.github/workflows/ci.yml`)
   - Тестирование с PostgreSQL
   - Запуск Django тестов
   - Проверка форматирования кода

2. **Docker Build** (`.github/workflows/docker.yml`)
   - Сборка Docker образа
   - Тестирование docker-compose
   - Проверка доступности API

3. **Code Quality** (`.github/workflows/code-quality.yml`)
   - Форматирование кода (Black)
   - Проверка импортов (isort)
   - Анализ безопасности зависимостей

### Команды для разработки
```bash
# Форматирование кода
poetry run black .

# Проверка импортов
poetry run isort .

# Запуск тестов
poetry run python manage.py test

# Запуск с покрытием
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```