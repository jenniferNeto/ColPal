# Base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the environment variable for the port
ENV PORT=8000

# Install system dependencies
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    gcc \
    libpq-dev \
    libc6-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

RUN python3 -m pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

# Copy project
COPY . /code/

EXPOSE 8000

RUN ["chmod", "+x", "/code/docker/docker-entrypoint.sh"]
ENTRYPOINT ["/code/docker/docker-entrypoint.sh"]
