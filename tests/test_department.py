from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test01TaskAPI:
    def test_01_get_task_user_list(self, client):
        """Запрос данных подразделений"""
        response = client.get("/api/v1/department/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/department/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/department/` возвращает ответ со статусом 401."
        )
