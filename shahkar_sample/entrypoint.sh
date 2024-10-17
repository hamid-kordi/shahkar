#!/bin/bash

# Start the Gunicorn server in the background
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application &

# Start the Celery worker
celery -A proj worker --concurrency=4
