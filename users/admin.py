from django.contrib import admin

from .models import User, Position


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name"]
    empty_value_display = "-empty-"


class PositionAdmin(admin.ModelAdmin):
    list_display = ['pos_id', 'name']
    empty_value_display = "-empty-"

admin.site.register(User, UserAdmin)
admin.site.register(Position, PositionAdmin)
