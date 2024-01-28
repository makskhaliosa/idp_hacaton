from datetime import timedelta
from typing import Dict, List

from django.db.models import Model
from django.utils import timezone

from core.choices import IdpStatuses


def default_end_date_plan():
    return timezone.now() + timedelta(days=30)


def find_differencies(initial: Model, updated: Model):
    """
    Return differencies between fields of two objects.

    Compares two dicts of original and updated objects.
    If any field differs, we take the updated value.
    Return dict with new values.
    """
    d1 = initial.__dict__
    d2 = updated.__dict__
    diffs = {k: v for k, v in d2.items() if v != d1[k]}
    if "_state" in diffs:
        # _state нам без надобности, поэтому убираем
        del diffs["_state"]
    return diffs


def get_idp_extra_info(idps: List[Model]) -> Dict[str, int]:
    """
    Generate extra fields for idp serializer.

    Count number of idps by statuses.
    """
    extra_info = {
        "in_total": 0,
        IdpStatuses.ACTIVE: 0,
        IdpStatuses.CLOSED: 0,
        IdpStatuses.OVERDUE: 0,
    }
    for idp in idps:
        if idp.status == IdpStatuses.ACTIVE:
            extra_info["in_total"] += 1
            extra_info[IdpStatuses.ACTIVE] += 1
        elif idp.status == IdpStatuses.CLOSED:
            extra_info["in_total"] += 1
            extra_info[IdpStatuses.CLOSED] += 1
        elif idp.status == IdpStatuses.OVERDUE:
            extra_info["in_total"] += 1
            extra_info[IdpStatuses.OVERDUE] += 1
    return extra_info
