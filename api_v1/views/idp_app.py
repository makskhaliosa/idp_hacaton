from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api_v1.filters import (
    IdpFilterSet,
    IdpOrderingFilter,
    TaskFilterSet,
    TaskOrderingFilter,
)
from api_v1.serializers.fields import (
    IDPasFieldSerializer,
    TaskAsFieldSerializer,
)
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
from core.choices import IdpStatuses
from core.utils import get_idp_extra_info, idp_status_order
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
    permission_classes = (IsAuthenticated,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, TaskOrderingFilter, DjangoFilterBackend)
    search_fields = ("^task_name", "^task_mentor__last_name")
    ordering_fields = (
        "task_name",
        "task_status",
        "task_end_date_plan",
        "task_start_date",
    )
    filterset_class = TaskFilterSet

    def get_queryset(self):
        idp_id = self.kwargs.get("idp_id")
        tasks = Task.objects.filter(idp=idp_id)
        return tasks

    @extend_schema(responses=IDPReadOnlySerializer)
    def list(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        idp = get_object_or_404(IDP, pk=tasks[0].idp_id)
        idp_data = IDPReadOnlySerializer(instance=idp).data
        if not tasks:
            return Response(data=idp_data)
        filtered_tasks = self.filter_queryset(tasks)
        tasks_data = TaskAsFieldSerializer(
            instance=filtered_tasks, many=True
        ).data
        idp_data["tasks"] = tasks_data
        return Response(data=idp_data)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated,)

    def download_file(self, request, file_id):
        file_obj = get_object_or_404(File, pk=file_id)
        file_content = file_obj.file.read()
        response = HttpResponse(
            file_content, content_type="application/octet-stream"
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{file_obj.file.name}"'
        return response


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)


class IDPViewSet(viewsets.ModelViewSet):
    queryset = IDP.objects.all()
    serializer_class = IDPReadOnlySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, IdpOrderingFilter, DjangoFilterBackend)
    search_fields = ("^name", "^employee__last_name")
    ordering_fields = (
        "name",
        "end_date_plan",
        "status",
        "employee__last_name",
        "employee__first_name",
    )
    filterset_class = IdpFilterSet

    def get_serializer_class(self):
        if self.request.method == "GET":
            return IDPReadOnlySerializer
        return CreateIDPSerializer

    def filter_queryset(self, queryset):
        filtered_queryset = super().filter_queryset(queryset)
        if self.request.query_params:
            if not self.request.query_params.get("ordering"):
                filtered_queryset.order_by(
                    idp_status_order,
                    "-end_date_plan",
                    "employee__last_name",
                    "employee__first_name",
                    "name",
                )
        else:
            filtered_queryset = filtered_queryset.order_by(
                idp_status_order,
                "-end_date_plan",
                "employee__last_name",
                "employee__first_name",
                "name",
            )
        return filtered_queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            idp_data = request.data

            employee_chief = User.objects.get(uid=idp_data["employee"]).chief

            if user != employee_chief:
                if idp_data["status"] not in (
                    IdpStatuses.DRAFT,
                    IdpStatuses.DRAFT_APPROVAL,
                ):
                    idp_data["status"] = IdpStatuses.DRAFT

            serializer = CreateIDPSerializer(data=idp_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(responses=IDPasFieldSerializer(many=True))
    @action(detail=False, url_path="private")
    def get_private_idps(self, request: Request):
        """Возвращает список личных ипр авторизованного пользователя."""
        idps = request.user.idps.all().order_by("-end_date_plan")
        filtered_idps = self.filter_queryset(idps)
        if filtered_idps:
            extra_info = get_idp_extra_info(filtered_idps)
            page = self.paginate_queryset(filtered_idps)
            if page:
                serializer = IDPasFieldSerializer(page, many=True)
                response = self.get_paginated_response(serializer.data)
            else:
                serializer = IDPasFieldSerializer(filtered_idps, many=True)
                response = Response(data=serializer.data)

            extra_info.update(response.data)
            response.data = extra_info
            return response
        return Response({"detail": "У вас еще нет ИПР."})

    @extend_schema(responses=IDPasFieldSerializer(many=True))
    @action(detail=False, url_path="subordinates")
    def get_subordinates_idps(self, request: Request):
        """Возвращает список ипр подчиненных."""
        subordinates = request.user.subordinates.all()
        if not subordinates:
            return Response({"detail": "У вас нет сотрудников."})
        idps = IDP.objects.filter(employee__in=subordinates).exclude(
            status=IdpStatuses.DRAFT
        )
        filtered_idps = self.filter_queryset(idps)

        if filtered_idps:
            extra_info = get_idp_extra_info(filtered_idps)
            page = self.paginate_queryset(filtered_idps)
            if page:
                serializer = IDPasFieldSerializer(page, many=True)
                response = self.get_paginated_response(serializer.data)
            else:
                serializer = IDPasFieldSerializer(filtered_idps, many=True)
                response = Response(data=serializer.data)

            extra_info.update(response.data)
            response.data = extra_info
            return response
        return Response({"detail": "У ваших сотрудников еще нет ИПР."})


class TaskNotificationViewSet(viewsets.ModelViewSet):
    queryset = TaskNotification.objects.all()
    serializer_class = TaskNotificationSerializer
    permission_classes = (IsAuthenticated,)


class IDPNotificationViewSet(viewsets.ModelViewSet):
    queryset = IdpNotification.objects.all()
    serializer_class = IDPNotificationSerializer
    permission_classes = (IsAuthenticated,)
