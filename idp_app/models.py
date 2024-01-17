from datetime import datetime
from django.db import models
import uuid

from core.choices import STATUS_CHOICES
from core.utils import default_end_date_plan
from users.models import User


class IDP(models.Model):
    idp_id = models.UUIDField(
        primary_key=True,
        verbose_name='idp_id',
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name='name',
        max_length=100,
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
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='idps'
    )
