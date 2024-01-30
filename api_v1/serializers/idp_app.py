from rest_framework import serializers

from core.utils import get_extensions
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
        fields = ("in_id", "notification", "idp", "date", "status")


class CreateIDPNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdpNotification
        fields = ("notification",)


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
            "task_note_mentor",
            "task_mentor_id",
            "file",
        )


class IDPReadOnlySerializer(serializers.ModelSerializer):
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
            "mentor",
            "notifications",
        )


class CreateIDPSerializer(serializers.ModelSerializer):
    notifications = CreateIDPNotificationSerializer(many=True, required=False)

    class Meta:
        model = IDP
        fields = (
            "name",
            "target",
            "status",
            "start_date",
            "end_date_plan",
            "end_date_fact",
            "employee",
            "mentor",
            "notifications",
        )

    def to_representation(self, instance):
        return IDPReadOnlySerializer(
            instance, context={"request": self.context.get("request")}
        ).data

    def create(self, validated_data):
        if "notifications" not in self.initial_data:
            idp = IDP.objects.create(**validated_data)

            return idp

        notifications = validated_data.pop("notifications")

        idp = IDP.objects.create(**validated_data)

        for notification in notifications:
            IdpNotification.objects.create(**notification, idp_id=idp.pk)

        return idp


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            "file_id",
            "file",
            "file_name",
            "file_type",
        )

    def validate(self, data):
        extensions, content_types = get_extensions()
        uploaded_file = data.get("file")
        if uploaded_file:
            content_type = uploaded_file.content_type
            if content_type not in content_types:
                raise serializers.ValidationError(
                    f"Непопустимый формат файла. "
                    f"Допустимые расширения: {', '.join(extensions)}"
                )
        return data

    def create(self, validated_data):
        uploaded_file = validated_data.get("file")
        file_name = uploaded_file.name
        content_type = uploaded_file.content_type
        return File.objects.create(
            file=uploaded_file, file_name=file_name, file_type=content_type
        )
