# LLM Project - Django приложение для онлайн-обучения

Проект представляет собой платформу для онлайн-обучения на основе Django REST API для управления курсами и уроками с функционалом подписок, платежей через Stripe, асинхронных задач через Celery и периодических задач через Celery Beat.

## 📋 Содержание

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Установка и запуск](#установка-и-запуск)
- [Docker развертывание](#docker-развертывание)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Документация](#api-документация)
- [Эндпоинты API](#эндпоинты-api)
- [Асинхронные задачи](#асинхронные-задачи)
- [Структура проекта](#структура-проекта)
- [Решение проблем](#решение-проблем)
- [Безопасность](#безопасность)

## 🚀 Технологии

| Технология | Назначение |
|------------|------------|
| Django 5.x + DRF | Бэкенд API |
| PostgreSQL | База данных |
| Redis | Брокер сообщений для Celery |
| Celery + Celery Beat | Асинхронные и периодические задачи |
| JWT | Аутентификация |
| Stripe | Платежная система |
| drf-yasg | Документация API (Swagger) |
| Poetry | Управление зависимостами |
| Docker + Docker Compose | Контейнеризация |
| Nginx | Веб-сервер и прокси |
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
- Установленный Docker Desktop
- 4+ GB свободной RAM
- WSL2 (для Windows)

### Быстрый запуск

```bash
# Клонировать репозиторий
git clone https://github.com/botnbot/LLM.git
cd LLM

# Настроить .env файл
cp .env_sample .env
# Отредактируйте .env - добавьте реальные значения

# Запустить все сервисы
docker compose up -d

# Создать суперпользователя
docker compose exec web python manage.py createsuperuser
Проверка работы
bash
# Проверить статус контейнеров
docker compose ps

# Посмотреть логи
docker compose logs -f

# Health check
curl http://localhost:8000/health/
Доступ к приложению
Сервис	URL
Swagger документация	http://localhost:8000/swagger/
Админ-панель	http://localhost:8000/admin/
Health check	http://localhost:8000/health/
Через Nginx	http://localhost
Особенности Docker реализации
✅ Все сервисы запускаются одной командой

✅ Healthcheck для проверки готовности БД и Redis

✅ Volumes для сохранения данных между перезапусками

✅ Собственная сеть для изоляции сервисов

✅ Переменные окружения из .env файла

✅ Автоматический перезапуск при падении (restart: unless-stopped)

✅ Автоматические миграции при старте веб-сервиса

✅ Создание группы модераторов при старте

🔄 CI/CD Pipeline
Проект настроен на автоматическое тестирование и деплой через GitHub Actions.

Workflow этапы
Этап	Описание
test	Запуск тестов, линтеров, Django checks
build	Сборка Docker образа и пуш в Docker Hub
deploy	Деплой на удаленный сервер через SSH

 ### GitHub Secrets

 #### Для работы CI/CD необходимо настроить следующие секреты:

Secret	Описание
SECRET_KEY	Django secret key
ALLOWED_HOSTS	Разрешённые хосты
POSTGRES_DB	Имя базы данных
POSTGRES_USER	Пользователь БД
POSTGRES_PASSWORD	Пароль БД
DEPLOY_HOST	IP адрес сервера
DEPLOY_USER	Пользователь SSH
SSH_PRIVATE_KEY	Приватный SSH ключ
DOCKER_USERNAME	Docker Hub username
DOCKER_PASSWORD	Docker Hub token
STRIPE_API_KEY	Stripe API ключ
📚 API Документация
После запуска приложения документация доступна по адресу:

Swagger UI: http://176.109.109.156:8000/swagger/

ReDoc: http://176.109.109.156:8000/redoc/

🔧 Установка и запуск (локальная разработка)
Требования
Python 3.12+

PostgreSQL

Redis (через WSL2 для Windows)

Poetry (опционально)

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
Создайте файл .env в корне проекта (скопируйте из .env_sample и заполните)


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
9. Заполнение тестовыми данными
bash
python manage.py create_payments
🛠️ Решение проблем
Контейнеры не запускаются
bash
# Очистить и пересобрать
docker compose down -v
docker compose build --no-cache
docker compose up -d
Swagger не открывается
bash
# Проверить логи
docker compose logs web --tail=50
Ошибка подключения к БД
bash
# Проверить, что PostgreSQL контейнер здоров
docker compose ps
docker compose logs db --tail=30
Ошибка "No space left on device"
bash
# Очистить Docker
docker system prune -a -f
🔐 Безопасность
Все секреты хранятся в GitHub Secrets

.env файл исключён из репозитория (в .gitignore)

DEBUG=False в production

ALLOWED_HOSTS настроен для production сервера

SSH ключи используются для безопасного деплоя

📁 Структура проекта
text
LLM/
├── .github/workflows/     # CI/CD конфигурации
├── config/                # Django настройки
│   ├── settings/          # Раздельные настройки
│   │   ├── base.py        # Базовые настройки
│   │   ├── local.py       # Локальная разработка
│   │   └── production.py  # Продакшн настройки
│   ├── urls.py            # URL конфигурация
│   └── wsgi.py            # WSGI конфигурация
├── materials/             # Приложение курсов и уроков
├── users/                 # Приложение пользователей
├── static/                # Статические файлы (собранные)
├── media/                 # Медиа файлы (пользовательские)
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Docker Compose конфигурация
├── nginx.conf             # Nginx конфигурация
├── pyproject.toml         # Poetry зависимости
├── poetry.lock            # Lock файл зависимостей
├── .env_sample            # Шаблон переменных окружения
└── .gitignore             # Git исключения

### Продакшн сервер

Проект развернут на сервере:

Сервис	URL
Swagger документация	http://176.109.109.156:8000/swagger/
Health check	http://176.109.109.156:8000/health/
Админ-панель	http://176.109.109.156:8000/admin/
📄 Лицензия
BSD License

