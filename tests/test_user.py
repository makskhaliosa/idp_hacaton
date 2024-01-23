from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test01UserAPI:
    def test_01_get_user(self, client):
        """запрос данных сотрудника при входе в сервис ИПР"""
        response = client.get("/api/v1/user/department/settings/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/user/department/settings/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/user/department/settings/` возвращает ответ со статусом 401."
        )

    def test_02_get_chief(self, client):
        response = client.get("/api/v1/idp/chief/list/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/idp/chief/list/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/idp/chief/list/` возвращает ответ со статусом 401."
        )

    def test_03_get_user_department(self, client):
        """Запрос списка сотрудников для создания ИПР"""
        response = client.get("/api/v1/user/department/employees/list/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/user/department/employees/list/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/user/department/employees/list/` возвращает ответ со статусом 401."
        )

    def test_04_get_user_company(self, client):
        """запрос списка сотрудников для выбора ментора"""
        response = client.get("/api/v1/user/company/employees/list/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/user/company/employees/list/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/user/company/employees/list/` возвращает ответ со статусом 401."
        )
