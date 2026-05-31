
# LLM Project - Django приложение для онлайн-обучения

Проект представляет собой платформу для онлайн-обучения на основе Django REST API для управления курсами и уроками с функционалом подписок, платежей через Stripe, асинхронных задач через Celery и периодических задач через Celery Beat.

[![CI/CD Pipeline](https://github.com/botnbot/LLM/actions/workflows/deploy.yml/badge.svg)](https://github.com/botnbot/LLM/actions/workflows/deploy.yml)

## 📋 Содержание

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Быстрый старт](#быстрый-старт)
- [Docker развертывание](#docker-развертывание)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Документация](#api-документация)
- [Эндпоинты API](#эндпоинты-api)
- [Структура проекта](#структура-проекта)
- [Решение проблем](#решение-проблем)
- [Безопасность](#безопасность)

## 🚀 Технологии

| Технология | Назначение |
|------------|------------|
| Django 5.x + DRF | Бэкенд API |
| PostgreSQL 15 | База данных |
| Redis 7 | Брокер сообщений для Celery |
| Celery 5.x + Celery Beat | Асинхронные и периодические задачи |
| JWT | Аутентификация |
| Stripe | Платежная система |
| drf-yasg | Документация API (Swagger) |
| Poetry | Управление зависимостями |
| Docker + Docker Compose | Контейнеризация |
| Nginx 1.25 | Веб-сервер и прокси |
| GitHub Actions | CI/CD пайплайн |

## 📦 Функциональность

### Пользователи
- Регистрация и аутентификация (JWT)
- Управление профилем
- Роли: пользователь, модератор
- Автоматическая блокировка неактивных пользователей (более 30 дней)

### Курсы и уроки
- CRUD операции для курсов и уроков
- Подписка на обновления курсов
- Отправка email уведомлений при обновлении курса
- Ограничение на частоту уведомлений (не чаще 1 раза в 4 часа)

### Платежи
- Интеграция со Stripe
- Создание платежных сессий
- Поддержка разных способов оплаты

### Асинхронные задачи
- Отправка email уведомлений
- Блокировка неактивных пользователей
- Периодические задачи через Celery Beat

## 🐳 Docker развертывание

### Предварительные требования
- Установленный Docker Desktop (24.0.0+)
- Docker Compose V2 (встроен в Docker Desktop)
- 4+ GB свободной RAM
- WSL2 (для Windows) или Linux/MacOS

### Быстрый запуск (локальная разработка)

```bash
# Клонировать репозиторий
git clone https://github.com/botnbot/LLM.git
cd LLM

# Настроить .env файл для локальной разработки
cp .env_sample .env.local

# Отредактируйте .env.local - добавьте реальные значения

# Запустить все сервисы в режиме разработки
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d

# Применить миграции
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py migrate

# Создать суперпользователя
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py createsuperuser

# Создать группы доступа
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py create_groups
Запуск в production режиме
bash
# Настроить production .env файл
cp .env_sample .env

# Заполните все production переменные

# Запустить production конфигурацию (явно указываем prod файл)
docker compose -f docker-compose.prod.yml up -d

# Выполнить миграции
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Собрать статику
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic
Проверка работы
bash
# Проверить статус контейнеров
docker compose -f docker-compose.yml -f docker-compose.local.yml ps

# Посмотреть логи всех сервисов
docker compose -f docker-compose.yml -f docker-compose.local.yml logs -f

# Посмотреть логи конкретного сервиса
docker compose -f docker-compose.yml -f docker-compose.local.yml logs web --tail=50

# Health check
curl http://localhost:8000/health/
Доступ к приложению
Сервис	Локальный URL	Production URL
Swagger документация	http://localhost:8000/swagger/	http://176.109.109.156:8000/swagger/
ReDoc	http://localhost:8000/redoc/	http://176.109.109.156:8000/redoc/
Админ-панель	http://localhost:8000/admin/	http://176.109.109.156:8000/admin/
Health check	http://localhost:8000/health/	http://176.109.109.156:8000/health/
Через Nginx	http://localhost	http://176.109.109.156
Важные особенности Docker конфигурации
Файл	Назначение	Когда использовать
docker-compose.yml	Базовая конфигурация для всех окружений	Всегда
docker-compose.local.yml	Override для разработки (hot-reload, debug tools)	Только локально: -f docker-compose.local.yml
docker-compose.prod.yml	Production конфигурация (gunicorn, без debug)	На сервере: -f docker-compose.prod.yml
⚠️ Важно:

❌ НЕ используйте docker-compose.override.yml - он автоматически применяется и может вызвать проблемы

✅ Всегда явно указывайте нужный compose файл с флагом -f

✅ Для production используйте ТОЛЬКО docker-compose.prod.yml

Особенности реализации:

✅ Все сервисы запускаются одной командой

✅ Healthcheck для проверки готовности БД и Redis

✅ Volumes для сохранения данных между перезапусками

✅ Собственная сеть для изоляции сервисов

✅ Переменные окружения из .env файла

✅ Автоматический перезапуск при падении (restart: unless-stopped)

✅ Раздельные настройки для local и production

🔄 CI/CD Pipeline
Проект настроен на автоматическое тестирование и деплой через GitHub Actions.

Workflow этапы
Этап	Описание	Инструменты
test-and-lint	Запуск тестов, линтеров, проверка стиля	pytest, flake8, black, isort
build-and-push	Сборка Docker образа и пуш в GHCR	Docker Buildx, GHCR
deploy	Деплой на удаленный сервер через SSH	SSH, Docker Compose
GitHub Secrets
Для работы CI/CD необходимо настроить следующие секреты:
Secret	Описание	Пример
SERVER_HOST	IP адрес сервера	176.109.109.156
SERVER_USER	Пользователь SSH	ubuntu
SSH_PRIVATE_KEY	Приватный SSH ключ	-----BEGIN RSA PRIVATE KEY-----
SERVER_PORT	SSH порт (опционально)	22
ENV_PRODUCTION	Полный .env файл (base64)	base64 encoded string
DJANGO_SECRET_KEY	Django secret key	django-insecure-...
ALLOWED_HOSTS	Разрешённые хосты	176.109.109.156,domain.com
DB_NAME	Имя базы данных	llm_db_prod
DB_USER	Пользователь БД	llm_user
DB_PASSWORD	Пароль БД	secure_password
CSRF_TRUSTED_ORIGINS	Доверенные origin	https://176.109.109.156
STRIPE_API_KEY	Stripe API ключ	sk_live_...
Настройка секретов:
bash
# 1. Создать production .env файл
cat > .env.production << 'EOF'
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=176.109.109.156
DB_NAME=llm_db_prod
DB_USER=llm_user
DB_PASSWORD=your-secure-password
EOF

# 2. Закодировать в base64
cat .env.production | base64 -w 0

# 3. Скопировать результат в GitHub Secret ENV_PRODUCTION
Процесс деплоя
При пуше в ветку main:

Автоматически запускаются тесты и линтеры

Собирается Docker образ (production stage)

Образ пушится в GitHub Container Registry (GHCR)

На сервер копируется .env файл

Деплоятся контейнеры с docker-compose.prod.yml

Выполняются миграции и сборка статики

Отправляется уведомление о статусе деплоя

Важно: Деплой всегда использует явный compose файл, исключая случайное применение override.

📚 API Документация
После запуска приложения документация доступна по адресу:

Swagger UI: http://176.109.109.156:8000/swagger/

ReDoc: http://176.109.109.156:8000/redoc/

🔧 Локальная разработка (без Docker)
Требования
Python 3.12+

PostgreSQL 15+

Redis 7+ (через WSL2 для Windows)

Poetry

1. Клонирование репозитория
bash
git clone https://github.com/botnbot/LLM.git
cd LLM
2. Установка зависимостей
bash
poetry install
poetry shell
3. Настройка базы данных PostgreSQL
sql
CREATE DATABASE llm_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE llm_db TO postgres;
4. Настройка переменных окружения
bash
cp .env_sample .env
# Отредактируйте .env, установите DEBUG=True для разработки
5. Настройка Redis
Windows (через WSL):

bash
# В PowerShell (администратор)
wsl --install

# В Ubuntu (WSL)
sudo apt update
sudo apt install redis-server -y
sudo sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/' /etc/redis/redis.conf
sudo sed -i 's/protected-mode yes/protected-mode no/' /etc/redis/redis.conf
sudo service redis-server start
redis-cli ping  # Должно вернуть PONG
Linux/Mac:

bash
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
redis-cli ping  # Должно вернуть PONG
6. Применение миграций
bash
python manage.py makemigrations
python manage.py migrate
7. Создание суперпользователя
bash
python manage.py createsuperuser
8. Создание групп доступа
bash
python manage.py create_groups
9. Запуск Celery worker (в отдельном терминале)
bash
celery -A config worker --loglevel=info
10. Запуск Celery Beat (в отдельном терминале)
bash
celery -A config beat --loglevel=info
11. Запуск сервера разработки
bash
python manage.py runserver
📁 Структура проекта
text
LLM/
├── .github/workflows/     # CI/CD конфигурации
│   └── deploy.yml         # GitHub Actions workflow
├── config/                # Django настройки
│   ├── settings/          # Раздельные настройки окружений
│   │   ├── base.py        # Базовые настройки
│   │   ├── local.py       # Локальная разработка (DEBUG=True)
│   │   └── production.py  # Продакшн настройки (DEBUG=False)
│   ├── urls.py            # URL конфигурация
│   ├── wsgi.py            # WSGI конфигурация
│   └── celery.py          # Celery конфигурация
├── materials/             # Приложение курсов и уроков
├── users/                 # Приложение пользователей
├── payments/              # Приложение платежей (Stripe)
├── static/                # Статические файлы (собранные)
├── media/                 # Медиа файлы (пользовательские)
├── nginx/                 # Nginx конфигурация
│   ├── default.conf       # Локальный nginx
│   └── nginx.prod.conf    # Production nginx
├── Dockerfile             # Docker образ (multi-stage)
├── docker-compose.yml     # Базовая Docker Compose конфигурация
├── docker-compose.local.yml # Override для локальной разработки
├── docker-compose.prod.yml  # Production конфигурация
├── pyproject.toml         # Poetry зависимости
├── poetry.lock            # Lock файл зависимостей
├── .env_sample            # Шаблон переменных окружения
├── .env.local.example     # Шаблон для локальной разработки
├── .gitignore             # Git исключения
└── README.md              # Документация
🛠️ Решение проблем
Контейнеры не запускаются
bash
# Очистить и пересобрать
docker compose down -v
docker compose build --no-cache
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d
Swagger не открывается
bash
# Проверить логи веб-сервиса
docker compose -f docker-compose.yml -f docker-compose.local.yml logs web --tail=50

# Убедиться, что drf-yasg установлен
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web pip list | grep drf-yasg
Ошибка подключения к БД
bash
# Проверить, что PostgreSQL контейнер здоров
docker compose -f docker-compose.yml -f docker-compose.local.yml ps
docker compose -f docker-compose.yml -f docker-compose.local.yml logs db --tail=30

# Проверить connection string в .env
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python -c "import os; print(os.environ.get('DB_HOST'))"
Celery задачи не выполняются
bash
# Проверить статус Celery worker
docker compose -f docker-compose.yml -f docker-compose.local.yml logs celery --tail=30

# Проверить подключение к Redis
docker compose -f docker-compose.yml -f docker-compose.local.yml exec redis redis-cli ping
Ошибка "No space left on device"
bash
# Очистить Docker
docker system prune -a -f

# Очистить volumes
docker volume prune -f
docker-compose.override.yml случайно применился
bash
# Удалить override файл если он существует
rm docker-compose.override.yml

# Или всегда явно указывать compose файлы
docker compose -f docker-compose.yml -f docker-compose.local.yml up
🔐 Безопасность
Принятые меры:
Все секреты хранятся в GitHub Secrets

.env файл исключён из репозитория (в .gitignore)

DEBUG=False в production

ALLOWED_HOSTS настроен для production сервера

SSH ключи используются для безопасного деплоя

JWT токены для аутентификации

CORS настроен для разрешенных доменов

SSL/TLS (планируется для домена)

Регулярные обновления зависимостей

Рекомендации:
bash
# Регулярно обновляйте зависимости
poetry update

# Проверяйте уязвимости
poetry run safety check

# Используйте надежные пароли
openssl rand -base64 32

# Включайте двухфакторную аутентификацию в GitHub
📄 Лицензия
BSD License. Подробнее в файле LICENSE.

👥 Контакты
Разработчик: @botnbot

Проект: LLM on GitHub

Production: http://176.109.109.156

## Основные исправления разметки:

1. **✅ Закрыты все блоки кода** - каждый блок начинается с ` ```bash ` и заканчивается ` ``` `
2. **✅ Исправлены незакрытые строки** - команды теперь внутри блоков кода
3. **✅ Убраны лишние пробелы** перед блоками кода
4. **✅ Исправлены SQL блоки** - использован `sql` вместо `bash`
5. **✅ EOF исправлен** - в heredoc используется `'EOF'` для предотвращения интерполяции
6. **✅ Вложенные списки** - исправлены отступы
7. **✅ Таблицы** - все таблицы правильно отформатированы
8. **✅ Эмодзи** - оставлены, но проверены на совместимость

Теперь markdown разметка полностью корректна и README будет правильно отображаться на GitHub!
This response is AI-generated, for reference only.
C:\Projects\LLM\README.md
LLM Project - Django приложение для онлайн-обучения
Проект представляет собой платформу для онлайн-обучения на основе Django REST API для управления курсами и уроками с функционалом подписок, платежей через Stripe, асинхронных задач через Celery и периодических задач через Celery Beat.

CICD Pipeline

📋 Содержание
Технологии
Функциональность
Быстрый старт
Docker развертывание
CI/CD Pipeline
API Документация
Эндпоинты API
Структура проекта
Решение проблем
Безопасность
🚀 Технологии
Технология	Назначение
Django 5.x + DRF	Бэкенд API
PostgreSQL 15	База данных
Redis 7	Брокер сообщений для Celery
Celery 5.x + Celery Beat	Асинхронные и периодические задачи
JWT	Аутентификация
Stripe	Платежная система
drf-yasg	Документация API (Swagger)
Poetry	Управление зависимостями
Docker + Docker Compose	Контейнеризация
Nginx 1.25	Веб-сервер и прокси
GitHub Actions	CI/CD пайплайн
📦 Функциональность
Пользователи
Регистрация и аутентификация (JWT)
Управление профилем
Роли: пользователь, модератор
Автоматическая блокировка неактивных пользователей (более 30 дней)
Курсы и уроки
CRUD операции для курсов и уроков
Подписка на обновления курсов
Отправка email уведомлений при обновлении курса
Ограничение на частоту уведомлений (не чаще 1 раза в 4 часа)
Платежи
Интеграция со Stripe
Создание платежных сессий
Поддержка разных способов оплаты
Асинхронные задачи
Отправка email уведомлений
Блокировка неактивных пользователей
Периодические задачи через Celery Beat
🐳 Docker развертывание
Предварительные требования
Установленный Docker Desktop (24.0.0+)
Docker Compose V2 (встроен в Docker Desktop)
4+ GB свободной RAM
WSL2 (для Windows) или Linux/MacOS
Быстрый запуск (локальная разработка)
# Клонировать репозиторий
git clone https://github.com/botnbot/LLM.git
cd LLM

# Настроить .env файл для локальной разработки
cp .env_sample .env.local
# Отредактируйте .env.local - добавьте реальные значения

# Запустить все сервисы в режиме разработки
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d

# Применить миграции
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py migrate

# Создать суперпользователя
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py createsuperuser

# Создать группы доступа
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py create_groups
Вижу проблему - в вашем README отсутствуют закрывающие обратные кавычки для блоков кода, и нет разделения между заголовками и содержимым. Вот исправленная полная версия:

markdown
# LLM Project - Django приложение для онлайн-обучения

Проект представляет собой платформу для онлайн-обучения на основе Django REST API для управления курсами и уроками с функционалом подписок, платежей через Stripe, асинхронных задач через Celery и периодических задач через Celery Beat.

[![CI/CD Pipeline](https://github.com/botnbot/LLM/actions/workflows/deploy.yml/badge.svg)](https://github.com/botnbot/LLM/actions/workflows/deploy.yml)

## 📋 Содержание

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Быстрый старт](#быстрый-старт)
- [Docker развертывание](#docker-развертывание)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Документация](#api-документация)
- [Эндпоинты API](#эндпоинты-api)
- [Структура проекта](#структура-проекта)
- [Решение проблем](#решение-проблем)
- [Безопасность](#безопасность)

## 🚀 Технологии

| Технология | Назначение |
|------------|------------|
| Django 5.x + DRF | Бэкенд API |
| PostgreSQL 15 | База данных |
| Redis 7 | Брокер сообщений для Celery |
| Celery 5.x + Celery Beat | Асинхронные и периодические задачи |
| JWT | Аутентификация |
| Stripe | Платежная система |
| drf-yasg | Документация API (Swagger) |
| Poetry | Управление зависимостями |
| Docker + Docker Compose | Контейнеризация |
| Nginx 1.25 | Веб-сервер и прокси |
| GitHub Actions | CI/CD пайплайн |

## 📦 Функциональность

### Пользователи
- Регистрация и аутентификация (JWT)
- Управление профилем
- Роли: пользователь, модератор
- Автоматическая блокировка неактивных пользователей (более 30 дней)

### Курсы и уроки
- CRUD операции для курсов и уроков
- Подписка на обновления курсов
- Отправка email уведомлений при обновлении курса
- Ограничение на частоту уведомлений (не чаще 1 раза в 4 часа)

### Платежи
- Интеграция со Stripe
- Создание платежных сессий
- Поддержка разных способов оплаты

### Асинхронные задачи
- Отправка email уведомлений
- Блокировка неактивных пользователей
- Периодические задачи через Celery Beat

## 🐳 Docker развертывание

### Предварительные требования
- Установленный Docker Desktop (24.0.0+)
- Docker Compose V2 (встроен в Docker Desktop)
- 4+ GB свободной RAM
- WSL2 (для Windows) или Linux/MacOS

### Быстрый запуск (локальная разработка)

```bash
# Клонировать репозиторий
git clone https://github.com/botnbot/LLM.git
cd LLM

# Настроить .env файл для локальной разработки
cp .env_sample .env.local
# Отредактируйте .env.local - добавьте реальные значения

# Запустить все сервисы в режиме разработки
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d

# Применить миграции
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py migrate

# Создать суперпользователя
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py createsuperuser

# Создать группы доступа
docker compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py create_groups
Запуск в production режиме
bash
# Настроить production .env файл
cp .env_sample .env

# Заполните все production переменные

# Запустить production конфигурацию
docker compose -f docker-compose.prod.yml up -d

# Выполнить миграции
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Собрать статику
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic
Проверка работы
bash
# Проверить статус контейнеров
docker compose -f docker-compose.yml -f docker-compose.local.yml ps

# Посмотреть логи всех сервисов
docker compose -f docker-compose.yml -f docker-compose.local.yml logs -f

# Health check
curl http://localhost:8000/health/
Доступ к приложению
Сервис	URL
Swagger документация	http://localhost:8000/swagger/
ReDoc	http://localhost:8000/redoc/
Админ-панель	http://localhost:8000/admin/
Health check	http://localhost:8000/health/
🔄 CI/CD Pipeline
Проект настроен на автоматическое тестирование и деплой через GitHub Actions.

Workflow этапы
Этап	Описание	Инструменты
test-and-lint	Запуск тестов, линтеров, проверка стиля	pytest, flake8, black, isort
build-and-push	Сборка Docker образа и пуш в GHCR	Docker Buildx, GHCR
deploy	Деплой на удаленный сервер через SSH	SSH, Docker Compose
GitHub Secrets
Для работы CI/CD необходимо настроить следующие секреты:

Secret	Описание
SERVER_HOST	IP адрес сервера
SERVER_USER	Пользователь SSH
SSH_PRIVATE_KEY	Приватный SSH ключ
ENV_PRODUCTION	Полный .env файл (base64)
Настройка секретов
bash
# 1. Создать production .env файл
cat > .env.production << 'EOF'
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=prod_db
DB_USER=prod_user
DB_PASSWORD=secure-password
EOF

# 2. Закодировать в base64
cat .env.production | base64 -w 0

# 3. Скопировать результат в GitHub Secret ENV_PRODUCTION
📚 API Документация
После запуска приложения документация доступна по адресу:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

🔧 Локальная разработка (без Docker)
Требования
Python 3.12+

PostgreSQL 15+

Redis 7+

Poetry

Установка
bash
# Клонирование репозитория
git clone https://github.com/botnbot/LLM.git
cd LLM

# Установка зависимостей
poetry install
poetry shell

# Настройка БД
createdb llm_db

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
Запуск Celery
bash
# В отдельном терминале
celery -A config worker --loglevel=info

# В еще одном терминале (для периодических задач)
celery -A config beat --loglevel=info
📁 Структура проекта
text
LLM/
├── .github/workflows/     # CI/CD конфигурации
│   └── deploy.yml
├── config/                # Django настройки
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── celery.py
├── materials/             # Приложение курсов и уроков
├── users/                 # Приложение пользователей
├── payments/              # Приложение платежей
├── Dockerfile
├── docker-compose.yml
├── docker-compose.local.yml
├── docker-compose.prod.yml
├── pyproject.toml
└── README.md
🛠️ Решение проблем
Контейнеры не запускаются
bash
docker compose down -v
docker compose build --no-cache
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d
Ошибка подключения к БД
bash
# Проверить статус PostgreSQL
docker compose ps
docker compose logs db --tail=30
Celery задачи не выполняются
bash
# Проверить статус Celery
docker compose logs celery --tail=30

# Проверить Redis
docker compose exec redis redis-cli ping
Очистка Docker
bash
# Очистить неиспользуемые данные
docker system prune -a -f

# Очистить volumes
docker volume prune -f
🔐 Безопасность
Принятые меры
Все секреты хранятся в GitHub Secrets

.env файл исключён из репозитория

DEBUG=False в production

ALLOWED_HOSTS настроен для production

SSH ключи для безопасного деплоя

JWT токены для аутентификации

Рекомендации
bash
# Регулярно обновляйте зависимости
poetry update

# Используйте надежные пароли
openssl rand -base64 32
📄 Лицензия
BSD License

👥 Контакты
Разработчик: @botnbot

Проект: LLM on GitHub

