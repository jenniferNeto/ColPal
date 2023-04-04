# Base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    gcc \
    libpq-dev \
    libc6-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy project
COPY . .

# Expose connection port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["./docker/backend-docker-entrypoint.sh"]
