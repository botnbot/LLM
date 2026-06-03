# LLM Project - Django приложение для онлайн-обучения
### Проект представляет собой платформу для онлайн-обучения на основе Django REST API для управления курсами и уроками с функционалом подписок, платежей через Stripe, асинхронных задач через Celery и периодических задач через Celery Beat.
[![CI/CD Pipeline](https://github.com/botnbot/LLM/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/botnbot/LLM/actions/workflows/ci-cd.yml)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)
## 📋 Содержание

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Docker развертывание](#docker-развертывание)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Документация](#api-документация)
- [Эндпоинты API](#эндпоинты-api)
- [Асинхронные задачи](#асинхронные-задачи)
- [Структура проекта](#структура-проекта)
- [Решение проблем](#решение-проблем)
- [Безопасность](#безопасность)

## Технологии

| Технология | Назначение                         |
|------------|------------------------------------|
| Django 5.x + DRF | Бэкенд API                         |
| PostgreSQL | База данных                        |
| Redis | Брокер сообщений для Celery        |
| Celery + Celery Beat | Асинхронные и периодические задачи |
| JWT | Аутентификация                     |
| Stripe | Платежная система                  |
| drf-yasg | Документация API (Swagger)         |
| Poetry | Управление зависимостями           |
| Docker + Docker Compose | Контейнеризация                    |
| Nginx | Веб-сервер и прокси                |
| GitHub Actions | CI/CD пайплайн                     |

# Функциональность

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

## Docker развертывание

### Предварительные требования
- Установленный Docker Desktop
- 4+ GB свободной RAM
- WSL2 (для Windows)

## Быстрый запуск


### Клонировать репозиторий
```bash
git clone https://github.com/botnbot/LLM.git
cd LLM
```

### Настроить .env файл
```bash
cp .env_sample .env
```

### Отредактировать .env - добавить реальные значения

### Запустить все сервисы
```bash
docker compose up -d
```

### Создать суперпользователя
```bash
docker compose exec web python manage.py createsuperuser
```

## Проверка работы

### Проверить статус контейнеров
```bash
docker compose ps
```

### Посмотреть логи
```bash
docker compose logs -f
```

# Health check
```bash
curl http://localhost:8000/health/
```
## Доступ к приложению
| Сервис                        | URL                         |
|-------------------------------|---------------------------------|
| Swagger документация          |	http://localhost:8000/swagger/ |
| Админ-панель                  |	http://localhost:8000/admin/ |
| Health check                  |	http://localhost:8000/health/ |
| Через Nginx |	http://localhost |
 #### Особенности Docker реализации
✅ Все сервисы запускаются одной командой

✅ Healthcheck для проверки готовности БД и Redis

✅ Volumes для сохранения данных между перезапусками

✅ Собственная сеть для изоляции сервисов

✅ Переменные окружения из .env файла

✅ Автоматический перезапуск при падении (restart: unless-stopped)

✅ Автоматические миграции при старте веб-сервиса

✅ Создание группы модераторов при старте

### CI/CD Pipeline
Проект настроен на автоматическое тестирование и деплой через GitHub Actions.
#### Workflow этапы
| Этап                        | Описание                         |
|-------------------------------|---------------------------------|
| test |	Запуск тестов, линтеров, Django checks |
| build |	Сборка Docker образа и пуш в Docker Hub |
| deploy |	Деплой на удаленный сервер через SSH |
## GitHub Secrets
Для работы CI/CD необходимо настроить следующие секреты:


| Secret       | Описание                         |
|--------------|---------------------------------|
| SECRET_KEY   |	Django secret key |
| ALLOWED_HOSTS |	Разрешённые хосты |
|POSTGRES_DB |	Имя базы данных|
|POSTGRES_USER |	Пользователь БД|
|POSTGRES_PASSWORD |	Пароль БД|
|DEPLOY_HOST |	IP адрес сервера|
|DEPLOY_USER |	Пользователь SSH|
|SSH_PRIVATE_KEY |	Приватный SSH ключ|
|DOCKER_USERNAME |	Docker Hub username|
|DOCKER_PASSWORD |	Docker Hub token|
|STRIPE_API_KEY	 | Stripe API ключ|
## API Документация
После запуска приложения документация доступна по адресу:

Swagger UI:
```bash
http://176.109.109.156:8000/swagger/
```
ReDoc:
```bash
http://176.109.109.156:8000/redoc/
```
# 🔧 Установка и запуск (локальная разработка)
#### Требования
Python 3.12+

PostgreSQL

Redis (через WSL2 для Windows)

Poetry (опционально)

### 1. Клонирование репозитория
```bash
git clone https://github.com/botnbot/LLM.git
cd LLM
```
### 2. Установка зависимостей
```bash
poetry install
poetry shell
```
### 3. Настройка базы данных PostgreSQL
```sql
CREATE DATABASE llm_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE llm_db TO postgres;
```
### 4. Настройка переменных окружения
Создайте файл .env в корне проекта (скопируйте из .env_sample):
```bash
env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=llm_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0

STRIPE_API_KEY=your-stripe-api-key
```
### 5. Настройка Redis

Windows (через WSL):

#### В PowerShell (администратор)
wsl --install

#### В Ubuntu (WSL)
```bash
sudo apt update
sudo apt install redis-server -y
sudo sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/' /etc/redis/redis.conf
sudo sed -i 's/protected-mode yes/protected-mode no/' /etc/redis/redis.conf
sudo service redis-server start
redis-cli ping  # Должно вернуть PONG
```

#### Linux/Mac
```bash
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
redis-cli ping  # Должно вернуть PONG
```
#### 6. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
7. Создание суперпользователя
```bash
python manage.py createsuperuser
```
8. Создание групп доступа
```bash
python manage.py create_groups
```
9. Заполнение тестовыми данными
```bash
python manage.py create_payments
```
# 🛠️ Решение проблем
### Контейнеры не запускаются
#### Очистить и пересобрать
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```
### Swagger не открывается
#### Проверить логи
```bash
docker compose logs web --tail=50
```
### Ошибка подключения к БД
#### Проверить, что PostgreSQL контейнер здоров
```bash
docker compose ps
docker compose logs db --tail=30
```
### Ошибка "No space left on device"
#### Очистить Docker
```bash
docker system prune -a -f
```
# 🔐 Безопасность
Все секреты хранятся в GitHub Secrets

.env файл исключён из репозитория (в .gitignore)

DEBUG=False в production

ALLOWED_HOSTS настроен для production сервера

SSH ключи используются для безопасного деплоя



```
📁 **Структура проекта**
LLM/
├── .github/
│ └── workflows/ # CI/CD конфигурации
├── config/ # Django настройки
│ ├── settings/ # Раздельные настройки
│ │ ├── base.py # Базовые настройки
│ │ ├── local.py # Локальная разработка
│ │ └── production.py # Продакшн настройки
│ ├── urls.py # URL конфигурация
│ └── wsgi.py # WSGI конфигурация
├── materials/ # Приложение курсов и уроков
├── users/ # Приложение пользователей
├── static/ # Статические файлы (собранные)
├── media/ # Медиа файлы (пользовательские)
├── Dockerfile # Docker образ
├── docker-compose.yml # Docker Compose конфигурация
├── nginx.conf # Nginx конфигурация
├── pyproject.toml # Poetry зависимости
├── poetry.lock # Lock файл зависимостей
├── .env_sample # Шаблон переменных окружения
└── .gitignore # Git исключения

```text


# Продакшн сервер

## Проект развернут на сервере:


| Сервис               | URL                                  |
|----------------------|--------------------------------------|
| Swagger документация | http://176.109.109.156:8000/swagger/ |
| Redoc документация   | http://176.109.109.156:8000/redoc/   |
| Health check         | http://176.109.109.156:8000/health/  |
| Админ-панель         | http://176.109.109.156:8000/admin/   |
###📄 Лицензия BSD License

