from django.contrib import admin

from .models import Company, Department, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "department")
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


admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Company, CompanyAdmin)
