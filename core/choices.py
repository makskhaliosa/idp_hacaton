from django.db import models


class IdpStatuses(models.TextChoices):
    """Status table for idps."""

    DRAFT = ("draft", "Черновик")
    DRAFT_APPROVAL = ("draft_approval", "Черновик (на согласовании)")
    ACTIVE = ("active", "Активные (в работе)")
    TWO_WEEKS = ("two_weeks", "Две недели до плановой даты выполнения")
    OVERDUE = ("overdue", "Просрочено")
    CANCELLED = ("cancelled", "Отменено")
    COMPLETED_APPROVAL = ("completed_approval", "Выполнено (на подтверждении)")
    CLOSED = ("closed", "Выполнено")


class TaskStatuses(models.TextChoices):
    """Status table for tasks."""

    DRAFT = ("draft", "Черновик")
    DRAFT_APPROVAL = ("draft_approval", "Черновик (на согласовании)")
    ACTIVE = (
        "active",
        "Активные (в работе)",
    )  # Если создано после создания ипр
    ACTIVE_WITH_IDP = (
        "active_with_idp",
        "Активные (в работе)",
    )  # Если создано вместе с ипр
    TWO_WEEKS = ("two_weeks", "Две недели до плановой даты выполнения")
    OVERDUE = ("overdue", "Просрочено")
    CANCELLED = ("cancelled", "Отменено")  # Если отменено отдельно от ипр
    CANCELLED_WITH_IDP = (
        "cancelled_with_idp",
        "Отменено",
    )  # Если отменено вместе с ипр
    COMPLETED_APPROVAL = ("completed_approval", "Выполнено (на подтверждении)")
    REJECTED = ("rejected", "Активные (в работе)")
    CLOSED = ("closed", "Выполнено")


class NotificationStatuses(models.TextChoices):
    """Status for link tables with notifications."""

    READ = "Read"
    UNREAD = "Unread"


class NotificationTriggers(models.TextChoices):
    """Triggers that create notifications."""

    # Уведомления после создания объектов

    IDP_CREATED = "Idp_created"  # Active Рук создал ИПР для сотрудника, уведомление сотруднику
    TASK_CREATED = "Task_created"  # Active Создать задачи, уведомление сотруднику и менторам
    TASK_CREATED_WITH_IDP = (
        "Task_created_with_idp"  # Active создано с ипр Уведомление менторам
    )

    # Уведомления после изменения объектов

    IDP_UPDATED = "Idp_updated"  # Редактировать ИПР, уведомление сотруднику
    TASK_COMMENT_ADDED = "Idp_comment_added"  # Добавить вопросы/замечания, уведомление сотруднику
    TASK_UPDATED = (
        "Idp_task_updated"  # Изменить список задач, уведомление сотруднику
    )
    TASK_ENDDATE_UPDATED = (
        "Task_enddate_plan_updated"  # Изменить плановую дату выполнения задач
    )
    MENTOR_CHANGED = "Mentor_changed"  # Изменить ментора

    # Уведомления после смены статусов

    IDP_TWO_WEEKS = "Two_weeks_before_idp_overdue"
    IDP_OVERDUE = "Idp_overdue"
    IDP_REQUEST_CREATED = "Idp_request_from_employee"  # Draft_approval Отправить заявку на ИПР, уведомление руку
    IDP_CANCELLED = "Idp_cancelled"  # Cancelled Отменить ИПР, уведомление сотруднику и менторам по таскам

    IDP_COMPLETED_APPROVAL = "Idp_close_request_created"  # Approved во всех задачах ИПР. Ментор согласовывает выполнение крайней задачи в ИПР сотрудника, уведомление руку
    IDP_CLOSED = "Idp_close_request_accepted"  # Closed Согласовать выполнение ИПР, уведомление сотруднику
    IDP_CLOSE_REJECTED = "Idp_close_request_rejected"  # Выполнение ИПР не подтверждено, уведомление сотруднику
    IDP_REQUEST_REJECTED = "Idp_request_rejected"  # Руководитель отклоняет план, уведомление сотруднику

    TASK_TWO_WEEKS = "Two_weeks_before_task_overdue"
    TASK_OVERDUE = "Task_overdue"
    TASK_CANCELLED = "Task_cancelled"
    TASK_CANCELLED_AFTER_IDP = "Task_cancelled_because_of_idp"
    TASK_COMPLETED_APPROVAL = "Task_close_request_created"
    TASK_CLOSED = "Task_closed"  # Approved Согласовать выполнение задачи, уведомление сотруднику
    TASK_CLOSE_REJECTED = "Task_close_rejected"  # Rejected close Ментор выбирает "Отправить на доработку", уведомление сотруднику


# Словари соответствия между статусами и триггерами для уведомлений
IdpNoteRelation = {
    IdpStatuses.DRAFT_APPROVAL: {
        "note": NotificationTriggers.IDP_REQUEST_CREATED,
        "receiver": ["chief"],
    },
    IdpStatuses.ACTIVE: {
        "note": NotificationTriggers.IDP_CREATED,
        "receiver": ["employee"],
    },
    IdpStatuses.TWO_WEEKS: {
        "note": NotificationTriggers.IDP_TWO_WEEKS,
        "receiver": ["emlpoyee", "chief"],
    },
    IdpStatuses.OVERDUE: {
        "note": NotificationTriggers.IDP_OVERDUE,
        "receiver": ["emlpoyee", "chief"],
    },
    IdpStatuses.COMPLETED_APPROVAL: {
        "note": NotificationTriggers.IDP_COMPLETED_APPROVAL,
        "receiver": ["chief"],
    },
    IdpStatuses.CLOSED: {
        "note": NotificationTriggers.IDP_CLOSED,
        "receiver": ["emlpoyee"],
    },
    IdpStatuses.CANCELLED: {
        "note": NotificationTriggers.IDP_CANCELLED,
        "receiver": ["emlpoyee"],
    },
    "updated": {
        "note": NotificationTriggers.IDP_UPDATED,
        "receiver": ["emlpoyee"],
    },
}

TaskNoteRelation = {
    TaskStatuses.ACTIVE: {
        "note": NotificationTriggers.TASK_CREATED,
        "receiver": ["employee", "mentor"],
    },
    TaskStatuses.ACTIVE_WITH_IDP: {
        "note": NotificationTriggers.TASK_CREATED_WITH_IDP,
        "receiver": ["mentor"],
    },
    TaskStatuses.TWO_WEEKS: {
        "note": NotificationTriggers.TASK_TWO_WEEKS,
        "receiver": ["emlpoyee"],
    },
    TaskStatuses.OVERDUE: {
        "note": NotificationTriggers.TASK_OVERDUE,
        "receiver": ["emlpoyee"],
    },
    TaskStatuses.COMPLETED_APPROVAL: {
        "note": NotificationTriggers.TASK_COMPLETED_APPROVAL,
        "receiver": ["chief"],
    },
    TaskStatuses.CLOSED: {
        "note": NotificationTriggers.TASK_CLOSED,
        "receiver": ["emlpoyee"],
    },
    TaskStatuses.CANCELLED: {
        "note": NotificationTriggers.TASK_CANCELLED,
        "receiver": ["emlpoyee", "mentor"],
    },
    TaskStatuses.CANCELLED_WITH_IDP: {
        "note": NotificationTriggers.TASK_CANCELLED_AFTER_IDP,
        "receiver": ["mentor"],
    },
    TaskStatuses.REJECTED: {
        "note": NotificationTriggers.TASK_CLOSE_REJECTED,
        "receiver": ["emlpoyee"],
    },
    "task_description": {
        "note": NotificationTriggers.TASK_UPDATED,
        "receiver": ["emlpoyee"],
    },
    "task_mentor_id_id": {
        "note": NotificationTriggers.MENTOR_CHANGED,
        "receiver": ["emlpoyee"],
    },
    "task_note_chief": {
        "note": NotificationTriggers.TASK_COMMENT_ADDED,
        "receiver": ["emlpoyee"],
    },
    "task_note_mentor": {
        "note": NotificationTriggers.TASK_COMMENT_ADDED,
        "receiver": ["emlpoyee"],
    },
    "task_end_date_plan": {
        "note": NotificationTriggers.TASK_ENDDATE_UPDATED,
        "receiver": ["emlpoyee"],
    },
}
