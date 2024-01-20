from django.db import models

STATUS_CHOICES = [
    ("active", "Активные"),
    ("completed", "Выполненные"),
    ("two_weeks", "Две недели до плановой даты выполнения"),
    ("overdue", "Просроченные"),
    ("canceled", "Отмененные"),
    ("closed", "Закрытые"),
    ("draft", "Черновик"),
]


class TaskStatuses(models.TextChoices):
    """Status table for tasks."""

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    NEED_DETAILS = "Need Details"
    REASSIGNED = "Reassigned"
    REVIEW = "Review"
    HOLD = "Hold"
    CLOSED = "Closed"


class NotificationStatuses(models.TextChoices):
    """Status for link tables with notifications."""

    READ = "Read"
    UNREAD = "Unread"


class NotificationTriggers(models.TextChoices):
    """Triggers that create notifications."""

    IDP_CREATED = "Idp_created"
    TASK_CREATED = "Task_created"
    TASK_DUE = "Task_due"
