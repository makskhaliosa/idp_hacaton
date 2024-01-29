from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    TWO_WEEKS = "Two weeks"
    OVERDUE = "Overdue"
    CANCELED = "Canceled"
    CLOSED = "Closed"
    DRAFT = "Draft"


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
