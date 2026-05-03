# LLM Project - Django приложение для онлайн-обучения 

Проект представляет собой платформу для онлайн-обучения на основе Django REST API приложения для управления
курсами и уроками с функционалом подписок, платежей через Stripe, асинхронных задач через Celery и периодических задач
через Celery Beat.

## 📋 Содержание

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Установка и запуск](#установка-и-запуск)
- [API Документация](#api-документация)
- [Эндпоинты API](#эндпоинты-api)
- [Асинхронные задачи](#асинхронные-задачи)
- [Структура проекта](#структура-проекта)
- [Решение проблем](#решение-типичных-проблем)
- [Безопасность](#безопасность)

## Технологии

- **Django** 5.x + Django REST Framework
- **PostgreSQL** - база данных
- **Redis** - брокер сообщений для Celery
- **Celery** + **Celery Beat** - асинхронные и периодические задачи
- **JWT** - аутентификация
- **Stripe** - платежная система
- **drf-yasg** - документация API (Swagger)
- **Poetry** - управление зависимостями

## Функциональность

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

## Установка и запуск

### Требования

- Python 3.12+
- PostgreSQL
- Redis (через WSL2 для Windows)
- Poetry (опционально)

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd LLM
```

### 2. Установка зависимостей
Используя Poetry:

poetry install
poetry shell

### 3. Настройка базы данных PostgreSQL
```sql
CREATE DATABASE LLM_project;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE LLM_project TO postgres;
```
### 4. Настройка переменных окружения
Создайте файл .env в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1

POSTGRES_DB=LLM_project
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0

STRIPE_API_KEY=your-stripe-api-key
```
#### Email настройки (опционально, в DEBUG режиме письма в консоль)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```
### 5. Настройка Redis
Для Windows (через WSL):
```bash
 В PowerShell (администратор)
wsl --install
```

#### В Ubuntu (WSL)
```bash
sudo apt update
sudo apt install redis-server -y
sudo sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/' /etc/redis/redis.conf
sudo sed -i 's/protected-mode yes/protected-mode no/' /etc/redis/redis.conf
sudo service redis-server start
redis-cli ping  # Должно вернуть PONG
```
#### Linux/Mac:
```bash
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
redis-cli ping  # Должно вернуть PONG
```
### 6. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```
### 7. Создание суперпользователя
```bash
python manage.py createsuperuser
```
### 8. Создание групп доступа
```bash
python manage.py create_groups
```
### 9. Заполнение тестовыми данными (опционально)
```bash
python manage.py create_payments
```