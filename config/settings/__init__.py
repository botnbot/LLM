"""
Автоматический выбор настроек в зависимости от окружения
"""
import os
import sys

# Получаем текущее окружение (по умолчанию local)
ENVIRONMENT = os.environ.get("ENV_NAME", "local")

# Загрузка соответствующих настроек
if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *

# Вывод информации о загруженном окружении
if 'runserver' in sys.argv or 'migrate' in sys.argv:
    print(f"Загружены настройки для окружения: {ENVIRONMENT}")