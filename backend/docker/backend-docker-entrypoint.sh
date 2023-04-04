#!/bin/bash

# If in production start the server
if [ $ENVIRONMENT == "production" ]; then
    python manage.py migrate
    python manage.py createadmin
    python manage.py runserver 0.0.0.0:8000
else
    # Return to original container to avoid exit code 0
    exec "$@"
fi