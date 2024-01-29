from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api_v1.serializers.idp_app import (
    DepartmentSerializer,
    IDPasFieldSerializer,
    IDPSerializer,
    TaskSerializer,
)
from core.choices import IdpStatuses
from core.utils import get_idp_extra_info
from idp_app.models import IDP, Task
from users.models import Department


class IDPViewSet(viewsets.ModelViewSet):
    queryset = IDP.objects.all()
    serializer_class = IDPSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("^name", "employee__last_name")
    ordering_fields = (
        "name",
        "end_date_plan",
        "status",
        "employee__last_name",
        "employee__first_name",
    )

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
        idps = (
            IDP.objects.filter(employee__in=subordinates)
            .exclude(status=IdpStatuses.DRAFT)
            .order_by("-end_date_plan", "employee__last_name")
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


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (AllowAny,)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)
