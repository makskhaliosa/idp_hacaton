from datetime import datetime, timedelta
from django.db import models
import uuid

from users.models import User


def default_end_date_plan():
    return timezone.now() + timedelta(days=30)


class IDP(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активные'),
        ('completed', 'Выполненные'),
        ('two_weeks', 'Две недели до плановой даты выполнения'),
        ('overdue', 'Просроченные'),
        ('canceled', 'Отмененные'),
        ('closed', 'Закрытые'),
        ('draft', 'Черновик')
    ]

    idp_id = models.UUIDField(
        primary_key=True,
        verbose_name='idp_id',
        default=uuid.uuid4,
        editable=False,
        blank=False,
    )
    name = models.CharField(
        verbose_name='name',
        max_length=100,
        blank=False,
        null=False
    )
    target = models.TextField(
        verbose_name='target',
        max_length=255,
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name='status',
        max_length=255,
        choices=STATUS_CHOICES,
        default='draft',
        blank=False,
        null=False
    )
    start_date = models.DateField(
        verbose_name='start_date',
        default=datetime.now,
        blank=True,
        null=True
    )
    end_date_plan = models.DateField(
        verbose_name='end_date_plan',
        default=default_end_date_plan,
        blank=True,
        null=True
    )
    end_date_fact = models.DateField(
        verbose_name='end_date_fact',
        blank=True,
        null=True
    )
    employee_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
    )
