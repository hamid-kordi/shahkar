import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shahkar_sample.settings")
app = Celery("shahkar_sample")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
