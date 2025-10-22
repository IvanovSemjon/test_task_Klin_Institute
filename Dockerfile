FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install

# Copy project
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]