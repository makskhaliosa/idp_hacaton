import logging
from itertools import chain
from typing import Any, Dict, List

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import Department, Position, User

from .idp_app import (
    IDPasFieldSerializer,
    IDPNotificationSerializer,
    TaskNotificationSerializer,
)

logger = logging.getLogger(__name__)


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


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения объектов User."""

    position = serializers.SlugRelatedField(
        slug_field="name", queryset=Position.objects.all()
    )
    chief = UserAsFieldSerializer()
    subordinates = UserAsFieldSerializer(many=True)
    department = serializers.SlugRelatedField(
        slug_field="dep_name", queryset=Department.objects.all()
    )
    idps = IDPasFieldSerializer(many=True)
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "uid",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "position",
            "chief",
            "department",
            "mentor_tasks",
            "idps",
            "subordinates",
            "notifications",
        )

    def get_notifications(self, obj: User) -> List[Dict[str, Any]]:
        """Объединяет уведомления по таскам и по ипр."""
        task_notes = obj.task_notices.all()
        idp_notes = obj.idp_notices.all()
        task_data = TaskNotificationSerializer(task_notes, many=True).data
        idp_data = IDPNotificationSerializer(idp_notes, many=True).data
        union_list = list(chain(task_data, idp_data))
        return union_list


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создния объектов User."""

    position = serializers.SlugRelatedField(
        slug_field="name", queryset=Position.objects.all()
    )
    department = serializers.SlugRelatedField(
        slug_field="dep_name", queryset=Department.objects.all()
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "uid",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "password",
            "department",
            "position",
        )

    def validate_password(self, data: str):
        validate_password(data, User)
        return data

    def create(self, validated_data: dict):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def to_representation(self, instance):
        serializer = UserSerializer(
            instance, context=self.context.get("request")
        )
        return serializer.data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления объектов User."""

    position = serializers.SlugRelatedField(
        slug_field="name", queryset=Position.objects.all(), required=False
    )
    chief = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    department = serializers.SlugRelatedField(
        slug_field="dep_name",
        queryset=Department.objects.all(),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "position",
            "chief",
            "department",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }
        read_only_fields = ("email", "mentor_tasks", "idps")

    def to_representation(self, instance):
        serializer = UserSerializer(
            instance, context=self.context.get("request")
        )
        return serializer.data
