from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api_v1.serializers.idp_app import IDPSerializer
from idp_app.models import IDP


class IDPViewSet(viewsets.ModelViewSet):
    queryset = IDP.objects.all()
    serializer_class = IDPSerializer

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
