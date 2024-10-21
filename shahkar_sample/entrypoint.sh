#!/bin/bash

# Start the Gunicorn server in the background
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application &

