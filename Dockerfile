FROM python:3.11-slim as builder

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# Создаем пользователя
RUN addgroup --system app && adduser --system --group app

# СОЗДАЕМ ДИРЕКТОРИЮ ДЛЯ ЛОГОВ И ДАЕМ ПРАВА ПОЛЬЗОВАТЕЛЮ app
RUN mkdir -p /var/log/django && chown -R app:app /var/log/django && chmod -R 755 /var/log/django

# Даем права на код
RUN chown -R app:app /code

USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]