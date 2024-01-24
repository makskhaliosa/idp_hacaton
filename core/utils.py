from datetime import timedelta

from django.db.models import Model
from django.utils import timezone


def default_end_date_plan():
    return timezone.now() + timedelta(days=30)


def find_differencies(initial: Model, updated: Model):
    """Return differencies between fields of two objects."""
    d1 = initial.__dict__
    d2 = updated.__dict__
    diffs = {k: v for k, v in d2.items() if v != d1[k]}
    if "_state" in diffs:
        del diffs["_state"]
    return diffs
