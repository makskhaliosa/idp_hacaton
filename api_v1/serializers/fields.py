from typing import Dict

from rest_framework import serializers

from idp_app.models import IDP, Task
from users.models import User


class UserAsFieldSerializer(serializers.ModelSerializer):
    """Сериализатор для User, где есть поле с отсылкой к User."""

    class Meta:
        model = User
        fields = (
            "uid",
            "first_name",
            "middle_name",
            "last_name",
        )
        read_only_fields = ("first_name", "middle_name", "last_name")


class IDPasFieldSerializer(serializers.ModelSerializer):
    """
    IDP сериализатор с определенными полями.

    Для включения в другие сериализаторы.
    """

    employee = serializers.SerializerMethodField()

    class Meta:
        model = IDP
        fields = ("idp_id", "name", "employee", "end_date_plan", "status")

    def get_employee(self, obj: IDP) -> Dict[str, str]:
        data = {
            "first_name": obj.employee.first_name,
            "last_name": obj.employee.last_name,
        }
        return data


class TaskAsFieldSerializer(serializers.ModelSerializer):
    """Сериализатор модели Task с определенными полями."""

    class Meta:
        model = Task
        fields = (
            "task_id",
            "task_name",
            "task_status",
            "task_start_date",
            "task_end_date_plan",
            "task_end_date_fact",
        )
