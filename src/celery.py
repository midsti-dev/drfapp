import django
from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

django.setup()

app = Celery("src")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()




