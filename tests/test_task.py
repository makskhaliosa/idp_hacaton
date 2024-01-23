from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test01TaskAPI:
    def test_01_get_task_user_list(self, client):
        """запрос данных сотрудника при входе в сервис ИПР"""
        response = client.get("/api/v1/task/employee/list/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/task/employee/list/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/task/employee/list/` возвращает ответ со статусом 401."
        )

    def test_02_get_all_task(self, client):
        """Запросить все задачи"""
        response = client.get("/api/v1/task/all/list/")
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            "Эндпоинт `/api/v1/task/all/list/` не найден. Проверьте настройки в "
            "*urls.py*."
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Проверьте, что GET-запрос неавторизованного пользователя к "
            "`/api/v1/task/all/list/` возвращает ответ со статусом 401."
        )

    # def test_03_get_task_details(self, client):
    #     """запрос данных сотрудника при входе в сервис ИПР"""
    #     tasks = create_tasks(admin_client)
    #     response = client.get(f'/api/v1/task/employee/details/{tasks[0]["id"]}/')
    #     assert response.status_code != HTTPStatus.NOT_FOUND, (
    #         'Эндпоинт `/api/v1/task/employee/details/{task_id}/` не найден. Проверьте настройки в '
    #         '*urls.py*.'
    #     )
    #     assert response.status_code == HTTPStatus.UNAUTHORIZED, (
    #         'Проверьте, что GET-запрос неавторизованного пользователя к '
    #         '`/api/v1/task/employee/details/{task_id}/` возвращает ответ со статусом 401.'
    #     )
