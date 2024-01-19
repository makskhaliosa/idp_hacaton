from django.contrib import admin

from .models import Company, Department, File, Task


class TaskAdmin(admin.ModelAdmin):
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
        "task_mentor_id",
    )
    search_fields = ("task_name",)
    empty_value_display = "-пусто-"


class FileAdmin(admin.ModelAdmin):
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


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("dep_id", "dep_name", "company_id")
    list_filter = ("company_id",)
    search_fields = ("dep_name",)
    empty_value_display = "-пусто-"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_id", "company_name")
    search_fields = ("company_name",)
    empty_value_display = "-пусто-"


admin.site.register(Task, TaskAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Company, CompanyAdmin)
