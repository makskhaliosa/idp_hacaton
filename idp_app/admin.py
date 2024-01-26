from django.contrib import admin

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


class TaskAdmin(EmptyFieldModel):
    list_display = (
        "task_id",
        "task_name",
        "task_description",
        "task_status",
        "mentor",
        "task_start_date",
        "task_end_date_plan",
        "task_end_date_fact",
        "task_note_employee",
        "task_note_cheif",
        "task_note_mentor",
        "task_mentor_id",
        "idp",
    )
    search_fields = ("task_name",)
    empty_value_display = "-пусто-"


class FileAdmin(EmptyFieldModel):
    list_display = (
        "file_id",
        "file_name",
        "file_link",
        "file_type",
        "file_task_id",
    )
    list_filter = (
        "file_type",
        "file_task_id",
    )
    search_fields = ("file_name",)
    empty_value_display = "-пусто-"


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
    empty_value_display = "-пусто-"
    inlines = [IDPNotificationTabularInline]


class NotificationAdmin(EmptyFieldModel):
    list_display = ("name", "trigger")
    list_filter = ("trigger",)
    search_fields = ("name", "trigger")
    empty_value_display = "-пусто-"


class IdpNoteAdmin(EmptyFieldModel):
    list_display = ("notification", "idp", "status", "date")
    list_filter = ("status",)
    search_fields = ("date", "idp__name", "notification__name")
    empty_value_display = "-пусто-"


class TaskNoteAdmin(EmptyFieldModel):
    list_display = ("notification", "task", "status", "date")
    list_filter = ("status",)
    search_fields = ("date", "task", "notification__name")
    empty_value_display = "-пусто-"


admin.site.register(Task, TaskAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(IDP, IDPAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(IdpNotification, IdpNoteAdmin)
admin.site.register(TaskNotification, TaskNoteAdmin)
