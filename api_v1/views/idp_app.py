from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_v1.serializers.idp_app import (
    DepartmentSerializer,
    IDPSerializer,
    TaskSerializer,
)
from core.choices import IdpStatuses
from core.utils import get_idp_extra_info
from idp_app.models import IDP, Task
from users.models import Department

from ..serializers.idp_app import IDPasFieldSerializer


class IDPViewSet(viewsets.ModelViewSet):
    queryset = IDP.objects.all()
    serializer_class = IDPSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("^name", "employee__last_name")
    ordering_fields = (
        "name",
        "end_date_plan",
        "status",
        "employee__last_name",
        "employee__first_name",
    )

    @action(detail=False, methods=["get"], url_path="chief/list")
    def idp_list(self, request, *args, **kwargs):
        """
        Запрос списка ИПР сотрудников отдела при входе в сервис ИПР.

        Mетод GET. Эндпоинт: api/v1/idp/chief/list
        """
        data = {"message": "Здесь будут данные."}
        return Response(data)

    @action(detail=False, methods=["get"], url_path="employee/list")
    def idp_retrieve(self, request, *args, **kwargs):
        """
        Запрос данных ИПР сотрудника при входе в сервис ИПР.

        Метод GET. Эндпоинт: api/v1/idp/employee/list
        """
        data = {"message": "Здесь будут данные."}
        return Response(data)

    @action(detail=False, methods=["post"], url_path="all/create")
    def idp_create(self, request, *args, **kwargs):
        """
        Сохранить новый ИПР сотрудника руководителем.

        Метод POST. Эндпоинт: api/v1/idp/all/create
        """
        data = {"message": "Здесь будут данные."}
        return Response(data)

    @action(detail=False, methods=["put"], url_path="status/update")
    def idp_update(self, request, *args, **kwargs):
        """
        Изменить статус ИПР.

        Метод PUT. Эндпоинт: api/v1/idp/status/update
        """
        data = {"message": "Здесь будут данные."}
        return Response(data)

    @action(detail=False, methods=["get"], url_path="all/list")
    def list_all(self, request, *args, **kwargs):
        """
        Запросить все ИПР.

        Метод GET. Эндпоинт: api/v1/idp/all/list
        """
        data = {"message": "Здесь будут данные."}
        return Response(data)

    @action(detail=False, methods=["update"], url_path="form/update")
    def update_form(self, request, *args, **kwargs):
        """
        Отредактировать поля ИПР.

        Метод Update. Эндпоинт: api/v1/idp/form/update
        """
        data = {"message": "Здесь будут данные."}
        return Response(data)

    @extend_schema(responses=IDPasFieldSerializer)
    @action(detail=False, url_path="subordinates")
    def get_subordinates_idps(self, request):
        """Return list of subordinates idps."""
        subordinates = request.user.subordinates.all()
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
                response.data.update(extra_info)
                return response

            serializer = IDPasFieldSerializer(filtered_idps, many=True)
            response = Response(data=serializer.data)
            response.data.update(extra_info)
            return response
        return Response({"detail": "Your employees don`t have idps yet."})


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (AllowAny,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)
