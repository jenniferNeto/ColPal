# Base image
FROM node:14.16.0-alpine

# Set working directory
WORKDIR /app

# Install node modules
COPY package*.json ./
RUN npm install

# Copy project
COPY . .

# Expose connection port
EXPOSE 3000

# Run entrypoint script
RUN chmod +x ./docker/frontend-docker-entrypoint.sh
ENTRYPOINT ["./docker/frontend-docker-entrypoint.sh"]

