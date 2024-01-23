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
    APPROVED = "Approved"


class NotificationStatuses(models.TextChoices):
    """Status for link tables with notifications."""

    READ = "Read"
    UNREAD = "Unread"


class NotificationTriggers(models.TextChoices):
    """Triggers that create notifications."""

    # Уведомления после создания объектов

    IDP_CREATED = "Idp_created"  # Active Рук создал ИПР для сотрудника, уведомление сотруднику
    TASK_CREATED = "Task_created"  # Создать задачи, уведомление сотруднику

    # Уведомления после изменения объектов

    IDP_UPDATED = "Idp_updated"  # Редактировать ИПР, уведомление сотруднику
    IDP_COMMENT_ADDED = "Idp_comment_added"  # Добавить вопросы/замечания, уведомление сотруднику
    TASKS_UPDATED = (
        "Idp_tasks_updated"  # Изменить список задач, уведомление сотруднику
    )
    TASK_ENDDATE_UPDATED = (
        "Task_enddate_plan_updated"  # Изменить плановую дату выполнения задач
    )
    MENTOR_CHANGED = "Mentor_changed"  # Изменить ментора

    # Уведомления после смены статусов

    IDP_REQUEST_CREATED = "Idp_request_from_employee"  # Draft Отправить заявку на ИПР, уведомление руку
    IDP_REQUEST_APPROVED = (
        "Idp_request_approved"  # Active Утвердить ИПР, уведомление сотруднику
    )
    IDP_CANCELLED = (
        "Idp_cancelled"  # Cancelled Отменить ИПР, уведомление сотруднику
    )
    IDP_CLOSE_REQUEST_CREATED = "Idp_close_request_created"  # Approved во всех задачах ИПР. Ментор согласовывает выполнение крайней задачи в ИПР сотрудника, уведомление руку
    IDP_CLOSE_REQUEST_ACCEPTED = "Idp_close_request_accepted"  # Согласовать выполнение ИПР, уведомление сотруднику
    IDP_CLOSE_REQUEST_REJECTED = "Idp_close_request_rejected"  # Выполнение ИПР не подтверждено, уведомление сотруднику
    IDP_REQUEST_REJECTED = "Idp_request_rejected"  # Руководитель отклоняет план, уведомление сотруднику
    TASK_REVIEW_REQUEST = (
        "Task_review_requested"  # Review Закрыть задачу, уведомление ментору
    )
    TASK_APPROVED = "Task_accepted"  # Approved Согласовать выполнение задачи, уведомление сотруднику
    TASK_REASSIGNED = "Task_rejected"  # Reassigned Ментор выбирает "Отправить на доработку", уведомление сотруднику
