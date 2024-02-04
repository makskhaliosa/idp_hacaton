import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idp.settings")

sched = Celery("idp")

sched.config_from_object("django.conf:settings", namespace="CELERY")

sched.autodiscover_tasks()
