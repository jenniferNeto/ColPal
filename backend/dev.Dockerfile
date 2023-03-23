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
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy project
COPY . /backend/

WORKDIR /backend/
EXPOSE 8000

RUN pip3 install -r requirements.txt