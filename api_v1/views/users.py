from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from api_v1.permissions import CreateUserPermission
from api_v1.serializers.users import (
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from users.models import User


@extend_schema_view(
    create=extend_schema(
        request=UserCreateSerializer, responses=UserSerializer
    ),
    partial_update=extend_schema(
        request=UserUpdateSerializer, responses=UserSerializer
    ),
)
class UserViewSet(ModelViewSet):
    """Вьюсет для объектов User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CreateUserPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("^last_name", "^first_name", "^middle_name")
    ordering_fields = ("last_name",)

    def get_serializer_class(self):
        if self.action == "update":
            return UserUpdateSerializer
        elif self.action == "create":
            return UserCreateSerializer
        return UserSerializer