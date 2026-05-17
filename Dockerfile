FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости с увеличенным таймаутом
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

RUN mkdir -p /code/static /code/media

EXPOSE 8000

RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    chown -R django:django /code

USER django