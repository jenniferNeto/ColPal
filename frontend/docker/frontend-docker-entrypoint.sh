#!/bin/sh

# If in production start the server
if [ "$ENVIRONMENT" = "production" ]; then
    # Build the deployment version of the frontend
    # npm run build

    # Serve the frontend
    # npm install -g serve
    serve -s build -l tcp://0.0.0.0:3000
else
    # Return to original container to avoid exit code 0
    exec "$@"
fi
