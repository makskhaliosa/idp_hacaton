from django.contrib import admin

from core.choices import IdpStatuses
from core.models import EmptyFieldModel, MinValidatedInlineMixIn

from .models import (
    IDP,
    File,
    IdpNotification,
    Notification,
    Task,
    TaskNotification,
)


class IDPNotificationTabularInline(
    admin.TabularInline, MinValidatedInlineMixIn
):
    model = IdpNotification
    validate_min = True
    min_num = 1


class TaskNotificationTabularInline(
    admin.TabularInline, MinValidatedInlineMixIn
):
    model = TaskNotification
    validate_min = True
    min_num = 1


class TaskAdmin(EmptyFieldModel):
    list_display = (
        "task_id",
        "task_name",
        "task_description",
        "task_status",
        "task_start_date",
        "task_end_date_plan",
        "task_end_date_fact",
        "task_note_employee",
        "task_note_cheif",
        "task_note_mentor",
        "task_mentor",
        "idp",
    )
    search_fields = ("task_name",)
    inlines = [TaskNotificationTabularInline]


class FileAdmin(EmptyFieldModel):
    list_display = (
        "file_id",
        "file_name",
        "file_type",
        "file_task_id",
    )
    list_filter = (
        "file_type",
        "file_task",
    )
    search_fields = ("file_name",)


class IDPAdmin(EmptyFieldModel):
    list_display = (
        "name",
        "target",
        "status",
        "employee",
        "start_date",
        "end_date_plan",
        "end_date_fact",
    )
    list_filter = ("status",)
    search_fields = ("name", "employee__last_name", "start_date")
    inlines = [IDPNotificationTabularInline]

    def save_model(self, request, obj, form, change):
        """
        Проверяет, был ли ипр создан рук-ом пользователя.

        Если нет, то задание является черновиком, который необходимо утвердить.
        """
        employee = obj.employee

        if request.user == employee.chief:
            obj.status = IdpStatuses.ACTIVE
        else:
            obj.status = IdpStatuses.DRAFT

        super().save_model(request, obj, form, change)


class NotificationAdmin(EmptyFieldModel):
    list_display = ("name", "trigger")
    list_filter = ("trigger",)
    search_fields = ("name", "trigger")


class IdpNoteAdmin(EmptyFieldModel):
    list_display = ("notification", "idp", "status", "date")
    list_filter = ("status",)
    search_fields = ("date", "idp__name", "notification__name")


class TaskNoteAdmin(EmptyFieldModel):
    list_display = ("notification", "task", "status", "date")
    list_filter = ("status",)
    search_fields = ("date", "task", "notification__name")


admin.site.register(Task, TaskAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(IDP, IDPAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(IdpNotification, IdpNoteAdmin)
admin.site.register(TaskNotification, TaskNoteAdmin)
