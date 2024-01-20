import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Таблица для сотрудников."""

    uid = models.UUIDField(
        primary_key=True,
        verbose_name="user_id",
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(verbose_name="first_name", max_length=100)
    middle_name = models.CharField(
        verbose_name="middle_name", max_length=100, blank=True
    )
    last_name = models.CharField(
        verbose_name="last_name", db_index=True, max_length=100
    )
    position = models.ForeignKey(
        "Position",
        on_delete=models.SET_NULL,
        verbose_name="user_position",
        related_name="users",
        null=True,
    )
    chief = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        verbose_name="chief",
        related_name="subordinates",
        blank=True,
        null=True,
    )
    mentor = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        verbose_name="mentor",
        related_name="students",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "User"
        verbose_name_plural = "Users"


class Position(models.Model):
    """Таблица с наименованием должностей сотрудников."""

    pos_id = models.AutoField(
        verbose_name="position_id",
        primary_key=True
    )
    name = models.CharField(
        verbose_name="position_name",
        max_length=255,
        unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Position"
        verbose_name_plural = "Positions"
