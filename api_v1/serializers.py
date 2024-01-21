from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User objects."""

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
