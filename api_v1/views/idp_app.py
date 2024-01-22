from api_v1.serializers.idp_app import TaskSerializer, DepartmentSerializer
from idp_app.models import Task, Department

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (AllowAny,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)