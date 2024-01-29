from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_v1.serializers.idp_app import (
    CreateIDPSerializer,
    DepartmentSerializer,
    FileSerializer,
    IDPNotificationSerializer,
    IDPReadOnlySerializer,
    NotificationSerializer,
    TaskNotificationSerializer,
    TaskSerializer,
)
from core.choices import StatusChoices
from idp_app.models import (
    IDP,
    File,
    IdpNotification,
    Notification,
    Task,
    TaskNotification,
)
from users.models import Department

User = get_user_model()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (AllowAny,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (AllowAny,)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (AllowAny,)


class IDPViewSet(viewsets.ModelViewSet):
    queryset = IDP.objects.all()
    serializer_class = IDPReadOnlySerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return IDPReadOnlySerializer
        return CreateIDPSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            idp_data = request.data

            employee_cheif = User.objects.get(uid=idp_data["employee"]).chief

            if user == employee_cheif:
                idp_data["status"] = StatusChoices.ACTIVE
            else:
                idp_data["status"] = StatusChoices.DRAFT

            serializer = CreateIDPSerializer(data=idp_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TaskNotificationViewSet(viewsets.ModelViewSet):
    queryset = TaskNotification.objects.all()
    serializer_class = TaskNotificationSerializer
    permission_classes = (AllowAny,)


class IDPNotificationViewSet(viewsets.ModelViewSet):
    queryset = IdpNotification.objects.all()
    serializer_class = IDPNotificationSerializer
    permission_classes = (AllowAny,)
