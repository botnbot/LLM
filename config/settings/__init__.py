"""
Автоматический выбор настроек в зависимости от окружения
"""
import os

# Получаем текущее окружение
ENVIRONMENT = os.environ.get("ENV_NAME", "local")

# Валидация окружения
VALID_ENVIRONMENTS = ["local", "production"]
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise ValueError(
        f"Неизвестное окружение: {ENVIRONMENT}. "
        f"Допустимые значения: {VALID_ENVIRONMENTS}"
    )

if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *

# Валидация окружения
VALID_ENVIRONMENTS = ["local", "staging", "production"]
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise ValueError(
        f"Неизвестное окружение: {ENVIRONMENT}. "
        f"Допустимые значения: {VALID_ENVIRONMENTS}"
    )

__all__ = [
    "BASE_DIR",
    "DEBUG",
    "SECRET_KEY",
    "ALLOWED_HOSTS",
    "DATABASES",
    "INSTALLED_APPS",
    "MIDDLEWARE",
    "ROOT_URLCONF",
    "WSGI_APPLICATION",
]

# Опционально: вывод информации о загруженном окружении
import sys
if 'runserver' in sys.argv or 'migrate' in sys.argv:
    print(f"Загружены настройки для окружения: {ENVIRONMENT}")