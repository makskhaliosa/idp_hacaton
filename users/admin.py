from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Company, Department, Position, User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "middle_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            "Job details",
            {"fields": ("department", "position", "chief", "mentor")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (
            "Personal info",
            {"fields": ("first_name", "middle_name", "last_name")},
        ),
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "department",
        "is_admin",
    )
    list_filter = ("is_admin", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "department")
    ordering = ("username",)
    filter_horizontal = ()
    empty_value_display = "-empty-"


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("dep_id", "dep_name", "company_id")
    list_filter = ("company_id",)
    search_fields = ("dep_name",)
    empty_value_display = "-пусто-"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("company_id", "company_name")
    search_fields = ("company_name",)
    empty_value_display = "-пусто-"


class PositionAdmin(admin.ModelAdmin):
    list_display = ("pos_id", "name")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Position, PositionAdmin)
