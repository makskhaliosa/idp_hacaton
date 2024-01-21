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
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name="user_department",
        null=True,
    )
    is_admin = models.BooleanField(verbose_name="user_is_admin", default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.position})"

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "User"
        verbose_name_plural = "Users"


class Position(models.Model):
    """Таблица с наименованием должностей сотрудников."""

    pos_id = models.AutoField(verbose_name="position_id", primary_key=True)
    name = models.CharField(
        verbose_name="position_name", max_length=255, unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Position"
        verbose_name_plural = "Positions"


class Company(models.Model):
    """Company table."""

    company_id = models.AutoField(
        primary_key=True,
        verbose_name="company_id",
    )
    company_name = models.CharField(
        verbose_name="company_name", max_length=200
    )

    class Meta:
        ordering = ("company_id",)
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.company_name


class Department(models.Model):
    """Department table."""

    dep_id = models.AutoField(primary_key=True, verbose_name="dep_id")
    dep_name = models.CharField(verbose_name="dep_name", max_length=400)
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="company_id",
    )

    class Meta:
        ordering = ("dep_id",)
        verbose_name = "Department"
        verbose_name_plural = "Departmens"

    def __str__(self) -> str:
        return self.dep_name
