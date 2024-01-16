import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uid = models.UUIDField(
        primary_key=True,
        verbose_name='user_id',
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(
        verbose_name='first_name',
        blank=False,
        max_length=100
    )
    middle_name = models.CharField(
        verbose_name='middle_name',
        max_length=100,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='last_name',
        blank=False,
        db_index=True,
        max_length=100
    )
    position = models.CharField(
        verbose_name='position',
        max_length=255
    )
    chief = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        verbose_name='chief',
        related_name='subordinates',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.position})'
