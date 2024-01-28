from rest_framework import serializers

from core.utils import get_extensions
from idp_app.models import IDP, File, Task
from users.models import Department


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
            "task_start_date",
            "task_end_date_plan",
            "task_end_date_fact",
            "task_note_employee",
            "task_note_cheif",
            "task_note_mentor",
            "task_mentor_id",
            "file",
        )


class IDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDP
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = (
            "file_id",
            "file",
            "file_link",
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
