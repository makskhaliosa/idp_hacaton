from rest_framework import viewsets
from rest_framework.permissions import AllowAny

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
from idp_app.models import (
    IDP,
    File,
    IdpNotification,
    Notification,
    Task,
    TaskNotification,
)
from users.models import Department


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


class TaskNotificationViewSet(viewsets.ModelViewSet):
    queryset = TaskNotification.objects.all()
    serializer_class = TaskNotificationSerializer
    permission_classes = (AllowAny,)


class IDPNotificationViewSet(viewsets.ModelViewSet):
    queryset = IdpNotification.objects.all()
    serializer_class = IDPNotificationSerializer
    permission_classes = (AllowAny,)
