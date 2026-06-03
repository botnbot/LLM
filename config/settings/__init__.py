"""
Автоматический выбор настроек в зависимости от окружения
"""
import os
import sys

_ENV = os.environ.get("ENV_NAME", "local")

VALID_ENVIRONMENTS = ["local", "production"]
if _ENV not in VALID_ENVIRONMENTS:
    raise ValueError(f"Неизвестное окружение: {_ENV}. Допустимые значения: {VALID_ENVIRONMENTS}")

if _ENV == "production":
    from .production import *
else:
    from .local import *

if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
    print(f"🚀 {_ENV.upper()} mode")