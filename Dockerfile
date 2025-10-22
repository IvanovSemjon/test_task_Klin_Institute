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

# Create wait script
RUN echo '#!/bin/sh\necho "Waiting for postgres..."\nuntil pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n  echo "PostgreSQL is unavailable - sleeping"\n  sleep 2\ndone\necho "PostgreSQL is up - executing command"\npoetry run python manage.py migrate\npoetry run python manage.py runserver 0.0.0.0:8000' > /app/wait-for-postgres.sh && chmod +x /app/wait-for-postgres.sh

# Run migrations and start server
CMD ["/app/wait-for-postgres.sh"]