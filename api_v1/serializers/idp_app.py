from rest_framework import serializers

from idp_app.models import (
    IDP,
    File,
    IdpNotification,
    Notification,
    Task,
    TaskNotification,
)
from users.models import Department


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("notice_id", "trigger", "name", "description")


class TaskNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskNotification
        fields = ("tn_id", "notification", "task", "date", "status")


class IDPNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdpNotification
        fields = ("in_id", "notifications", "idp", "date", "status")


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("dep_id", "dep_name", "company_id")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
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
            "task_note_cheif",
            "task_note_mentor",
            "task_mentor_id",
        )


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            "file_id",
            "file_name",
            "file_link",
            "file_type",
            "file_task_id",
        )


class IDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDP
        fields = (
            "idp_id",
            "name",
            "target",
            "status",
            "start_date",
            "end_date_plan",
            "end_date_fact",
            "employee",
            "notifications",
        )
