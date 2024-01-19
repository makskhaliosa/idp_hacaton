from datetime import timedelta

from django.utils import timezone


def default_end_date_plan():
    return timezone.now() + timedelta(days=30)
