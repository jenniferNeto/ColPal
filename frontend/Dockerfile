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
RUN npm run build
 # Serve the frontend
RUN npm install -g serve

# Run entrypoint script
ENTRYPOINT ["./docker/frontend-docker-entrypoint.sh"]

