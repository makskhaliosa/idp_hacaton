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


class UserRoles:
    chief: str = "chief"
    employee: str = "employee"
    mentor: str = "mentor"


# Словари соответствия между статусами и триггерами для уведомлений
IdpNoteRelation = {
    IdpStatuses.DRAFT_APPROVAL: {
        "note": NotificationTriggers.IDP_REQUEST_CREATED,
        "receiver": [UserRoles.chief],
        "message": {
            UserRoles.chief: (
                "Вам отправлен на согласование новый план развития"
            )
        },
    },
    IdpStatuses.ACTIVE: {
        "note": NotificationTriggers.IDP_CREATED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Вам создан новый план развития"},
    },
    IdpStatuses.TWO_WEEKS: {
        "note": NotificationTriggers.IDP_TWO_WEEKS,
        "receiver": [UserRoles.employee, UserRoles.chief],
        "message": {
            UserRoles.employee: (
                "Приближается срок выполнения вашего плана развития"
            ),
            UserRoles.chief: (
                "Приближается срок выполнения плана развития (<<сотрудник>>)"
            ),
        },
    },
    IdpStatuses.OVERDUE: {
        "note": NotificationTriggers.IDP_OVERDUE,
        "receiver": [UserRoles.employee, UserRoles.chief],
        "message": {
            UserRoles.employee: (
                "Просрочен срок выполнения вашего плана развития"
            ),
            UserRoles.chief: (
                "Просрочен срок выполнения плана развития (<<сотрудник>>)"
            ),
        },
    },
    IdpStatuses.COMPLETED_APPROVAL: {
        "note": NotificationTriggers.IDP_COMPLETED_APPROVAL,
        "receiver": [UserRoles.chief],
        "message": {
            UserRoles.chief: (
                "Вам отправлен на подтверждение выполненный план развития "
                "(<<сотрудник>>)"
            )
        },
    },
    IdpStatuses.CLOSED: {
        "note": NotificationTriggers.IDP_CLOSED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Ваш план развития выполнен"},
    },
    IdpStatuses.CANCELLED: {
        "note": NotificationTriggers.IDP_CANCELLED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Ваш план развития отменен"},
    },
    "updated": {
        "note": NotificationTriggers.IDP_UPDATED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Ваш план развития обновлен"},
    },
}

TaskNoteRelation = {
    TaskStatuses.ACTIVE: {
        "note": NotificationTriggers.TASK_CREATED,
        "receiver": [UserRoles.employee, UserRoles.mentor],
        "message": {
            UserRoles.employee: "В ваш план развития добавлена новая задача",
            UserRoles.mentor: "Вы назначены ментором задачи (<<сотрудник>>)",
        },
    },
    TaskStatuses.ACTIVE_WITH_IDP: {
        "note": NotificationTriggers.TASK_CREATED_WITH_IDP,
        "receiver": [UserRoles.mentor],
        "message": {
            UserRoles.mentor: "Вы назначены ментором задачи (<<сотрудник>>"
        },
    },
    TaskStatuses.TWO_WEEKS: {
        "note": NotificationTriggers.TASK_TWO_WEEKS,
        "receiver": [UserRoles.employee],
        "message": {
            UserRoles.employee: "Приближается срок выполнения вашей задачи"
        },
    },
    TaskStatuses.OVERDUE: {
        "note": NotificationTriggers.TASK_OVERDUE,
        "receiver": [UserRoles.employee],
        "message": {
            UserRoles.employee: "Просрочен срок выполнения вашей задачи"
        },
    },
    TaskStatuses.COMPLETED_APPROVAL: {
        "note": NotificationTriggers.TASK_COMPLETED_APPROVAL,
        "receiver": [UserRoles.mentor],
        "message": {
            UserRoles.mentor: (
                "Вам отправлена на подтверждение выполненная задача"
            )
        },
    },
    TaskStatuses.CLOSED: {
        "note": NotificationTriggers.TASK_CLOSED,
        "receiver": [UserRoles.employee],
        "message": {
            UserRoles.employee: "Выполнение вашей задачи подтверждено"
        },
    },
    TaskStatuses.CANCELLED: {
        "note": NotificationTriggers.TASK_CANCELLED,
        "receiver": [UserRoles.employee, UserRoles.mentor],
        "message": {
            UserRoles.employee: "Ваша задача отменена",
            UserRoles.mentor: "Задача (<<сотрудник>>) отменена",
        },
    },
    TaskStatuses.CANCELLED_WITH_IDP: {
        "note": NotificationTriggers.TASK_CANCELLED_AFTER_IDP,
        "receiver": [UserRoles.mentor],
        "message": {UserRoles.mentor: "Задача (<<сотрудник>>) отменена"},
    },
    TaskStatuses.REJECTED: {
        "note": NotificationTriggers.TASK_CLOSE_REJECTED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Ваша задача возвращена на доработку"},
    },
    "task_description": {
        "note": NotificationTriggers.TASK_UPDATED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Ваша задача обновлена"},
    },
    "task_mentor_id": {
        "note": NotificationTriggers.MENTOR_CHANGED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Ваш ментор изменен"},
    },
    "task_note_chief": {
        "note": NotificationTriggers.TASK_COMMENT_ADDED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Добавлен комментарий"},
    },
    "task_note_mentor": {
        "note": NotificationTriggers.TASK_COMMENT_ADDED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Добавлен комментарий"},
    },
    "task_end_date_plan": {
        "note": NotificationTriggers.TASK_ENDDATE_UPDATED,
        "receiver": [UserRoles.employee],
        "message": {UserRoles.employee: "Изменена дата заверщения задачи"},
    },
}
