# syntax=docker/dockerfile:1

############################################
# 1) Builder image + deps
############################################

FROM python:3.12.11-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install poetry & configure
RUN pip install poetry && poetry config virtualenvs.in-project true

# Copy only dependency files first (better caching)
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

# Copy source code
COPY . .

############################################
# 2) Runtime
############################################

FROM python:3.12.11-slim-bookworm

WORKDIR /app

# Copy virtual environment & project files from builder
COPY --from=builder /app /app

# Set Python options for cleaner logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Add dbmate
ADD https://github.com/amacneil/dbmate/releases/download/v2.28.0/dbmate-linux-amd64 /usr/local/bin/dbmate
RUN chmod +x /usr/local/bin/dbmate

# Expose ports for FastAPI
EXPOSE 8080

# No CMD here—let Fly processes control commands
