from datetime import timedelta
from typing import Dict, List

from django.db.models import Model
from django.utils import timezone

from core.choices import IdpStatuses


def default_end_date_plan():
    return timezone.now() + timedelta(days=30)


def find_differencies(initial: Model, updated: Model):
    """
    Возвращает различия между полями двух объектов.

    Сравнивает два dict исходного и обновленного объектов.
    Если какое-либо поле отличается, мы берем обновленное значение.
    Возвращает dict с новыми значениями.
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
    Генерирует дополнительные поля для ответа на запрос ИПР.

    Считает количество ипр по статусам.
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
