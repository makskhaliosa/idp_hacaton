import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from core.choices import (
    STATUS_CHOICES,
    NotificationStatuses,
    NotificationTriggers,
    TaskStatuses,
)
from core.utils import default_end_date_plan

User = get_user_model()


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
        verbose_name="target", max_length=255, blank=True, null=True
    )
    status = models.CharField(
        verbose_name="status",
        max_length=255,
        choices=STATUS_CHOICES,
        default="draft",
    )
    start_date = models.DateTimeField(
        verbose_name="start_date", default=datetime.now, blank=True, null=True
    )
    end_date_plan = models.DateTimeField(
        verbose_name="end_date_plan",
        default=default_end_date_plan,
        blank=True,
        null=True,
    )
    end_date_fact = models.DateTimeField(
        verbose_name="end_date_fact", blank=True, null=True
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="idps"
    )
    notifications = models.ManyToManyField(
        "Notification",
        through="IdpNotification",
        verbose_name="notifications",
        blank=True,
    )

    class Meta:
        ordering = ("name", "start_date")
        verbose_name = "IDP"
        verbose_name_plural = "IDPs"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_fileds = kwargs.get("update_fields")
        print(update_fileds)


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
        blank=True,
        null=True,
    )
    task_note_cheif = models.CharField(
        verbose_name="task_note_cheif", max_length=10000, blank=True, null=True
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
    idp = models.ForeignKey(
        IDP, on_delete=models.CASCADE, related_name="tasks", verbose_name="idp"
    )
    notifications = models.ManyToManyField(
        "Notification",
        through="TaskNotification",
        verbose_name="notifications",
        blank=True,
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


class Notification(models.Model):
    """Notifications table."""

    notice_id = models.AutoField(
        primary_key=True, verbose_name="notification_id"
    )
    trigger = models.CharField(
        verbose_name="notification_trigger",
        choices=NotificationTriggers,
        default=NotificationTriggers.IDP_CREATED,
        max_length=255,
    )
    name = models.CharField(verbose_name="notification_name", max_length=255)
    description = models.TextField(
        verbose_name="notification_description", blank=True, null=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self) -> str:
        return self.name


class TaskNotification(models.Model):
    """Link table for task related notifications and users."""

    tn_id = models.BigAutoField(
        primary_key=True, verbose_name="notification_user_id"
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="notice_tasks",
        verbose_name="notification",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_notices",
        verbose_name="task",
    )
    date = models.DateTimeField(
        verbose_name="notification_sent_datetime", auto_now_add=True
    )
    status = models.CharField(
        verbose_name="notification_status",
        choices=NotificationStatuses,
        max_length=40,
        default=NotificationStatuses.UNREAD,
    )

    def __str__(self) -> str:
        return f"{self.notification} {self.task}"


class IdpNotification(models.Model):
    """Link table for idp related notifications and users."""

    in_id = models.BigAutoField(
        primary_key=True, verbose_name="notification_user_id"
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="notice_idps",
        verbose_name="notification",
    )
    idp = models.ForeignKey(
        IDP,
        on_delete=models.CASCADE,
        related_name="idp_notices",
        verbose_name="idp",
    )
    date = models.DateTimeField(
        verbose_name="notification_sent_datetime", auto_now_add=True
    )
    status = models.CharField(
        verbose_name="notification_status",
        choices=NotificationStatuses,
        max_length=40,
        default=NotificationStatuses.UNREAD,
    )

    def __str__(self) -> str:
        return f"{self.notification} {self.idp}"
