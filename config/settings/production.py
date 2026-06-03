"""
Настройки для PRODUCTION
Все секреты берутся из переменных окружения (GitHub Secrets)
"""
from .base import *
import os

def require_env(var_name: str) -> str:
    """Получить обязательную переменную окружения"""
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f" {var_name} не задан!")
    return value

DEBUG = False
SECRET_KEY = require_env("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
if not ALLOWED_HOSTS or ALLOWED_HOSTS == [""]:
    raise RuntimeError("ALLOWED_HOSTS не может быть пустым!")

# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": require_env("POSTGRES_DB"),
        "USER": require_env("POSTGRES_USER"),
        "PASSWORD": require_env("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

# SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = require_env("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = require_env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = require_env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# Redis & Celery
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = os.getenv("REDIS_DB", "0")

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
    }
}

STATIC_ROOT = '/code/static'
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
MEDIA_ROOT = '/code/media'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/django/error.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["file"], "level": "WARNING"},
}

STRIPE_API_KEY = require_env("STRIPE_API_KEY")

print("🚀 PRODUCTION mode")