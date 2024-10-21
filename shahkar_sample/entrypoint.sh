#!/bin/bash

# Start the Gunicorn server in the background
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application &

# locust -f test_get_data.py --worker --master-host=127.0.0.1 --logfile locust.log
#locust -f test_get_data.py --master --web-port 8081 --logfile locust.log
