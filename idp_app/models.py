import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from core.choices import STATUS_CHOICES
from core.utils import default_end_date_plan

User = get_user_model()


class TaskStatuses(models.TextChoices):
    """Status table for tasks."""

    OPEN = ("Open",)
    IN_PROGRESS = ("In Progress",)
    NEED_DETAILS = ("Need Details",)
    REASSIGNED = ("Reassigned",)
    REVIEW = ("Review",)
    HOLD = ("Hold",)
    CLOSED = "Closed"


class IDP(models.Model):
    """IDP table."""

    idp_id = models.UUIDField(
        primary_key=True,
        verbose_name="idp_id",
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name="name",
        max_length=100,
    )
    target = models.TextField(
        verbose_name="target",
        max_length=255,
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name="status",
        max_length=255,
        choices=STATUS_CHOICES,
        default="draft",
    )
    start_date = models.DateTimeField(
        verbose_name="start_date",
        default=datetime.now,
        blank=True,
        null=True
    )
    end_date_plan = models.DateTimeField(
        verbose_name="end_date_plan",
        default=default_end_date_plan,
        blank=True,
        null=True,
    )
    end_date_fact = models.DateTimeField(
        verbose_name="end_date_fact",
        blank=True,
        null=True
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="idps"
    )


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


class Task(models.Model):
    """Tasks table."""

    task_id = models.AutoField(primary_key=True, verbose_name="task_id")
    task_name = models.CharField(verbose_name="task_name", max_length=150)
    task_description = models.CharField(
        verbose_name="task_description",
        max_length=10000,
    )
    task_status = models.CharField(
        verbose_name="task_status",
        max_length=40,
        choices=STATUS_CHOICES,
        default=TaskStatuses.OPEN,
    )
    task_start_date = models.DateTimeField(
        verbose_name="task_start_date",
    )
    task_end_date_plan = models.DateTimeField(
        verbose_name="task_end_date_plan",
        blank=True,
    )
    task_end_date_fact = models.DateTimeField(
        verbose_name="task_end_date_fact", blank=True, null=True
    )
    task_note_employee = models.CharField(
        verbose_name="task_note_employee",
        max_length=10000,
    )
    task_note_cheif = models.CharField(
        verbose_name="task_note_cheif",
        max_length=10000,
    )
    task_note_mentor = models.CharField(
        verbose_name="task_note_mentor", max_length=10000, blank=False
    )
    task_mentor_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="task_mentor_id",
        related_name="mentor_tasks",
        null=True,
    )

    class Meta:
        ordering = ("task_id",)
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return f"Task №{self.task_id}"


class File(models.Model):
    """Files table."""

    file_id = models.AutoField(primary_key=True, verbose_name="file_id")
    file_name = models.CharField(verbose_name="file_name", max_length=100)
    file_link = models.URLField(verbose_name="file_link", max_length=5000)
    file_type = models.CharField(verbose_name="file_type", max_length=10)
    file_task_id = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name="file_task_id"
    )

    class Meta:
        ordering = ("file_id",)
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self) -> str:
        return self.file_name
