FROM python:3.12-slim

WORKDIR /code

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копирование проекта
COPY . .

# Открываем порт
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]