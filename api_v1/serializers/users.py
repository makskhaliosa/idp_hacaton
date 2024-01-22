from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import Department, Position, User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for getting or updating User objects."""

    position = serializers.SlugRelatedField(
        slug_field="name", queryset=Position.objects.all(), required=False
    )
    chief = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    mentor = serializers.PrimaryKeyRelatedField(
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
            "uid",
            "first_name",
            "middle_name",
            "last_name",
            "position",
            "chief",
            "mentor",
            "department",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating User objects."""

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
            "username",
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
