from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test01IDPAPI:
    def test_01_get_idp_user_list(self, client):
        """Запрос данных ИПР сотрудника при входе в сервис ИПР"""
        response = client.get("/api/v1/idp/employee/list/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/idp/employee/list/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/idp/employee/list/` возвращает ответ со статусом 401."
        )

    def test_02_get_all_idp(self, client):
        """Запросить все ИПР"""
        response = client.get("/api/v1/idp/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/idp/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/idp/` возвращает ответ со статусом 401."
        )
