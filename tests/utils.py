from http import HTTPStatus


def create_idp(client):
    result = []
    data = {
        "name": "string",
        "target": "string",
        "status": "draft",
        "start_date": "2024-02-01T11:49:10.291Z",
        "end_date_plan": "2024-02-01T11:49:10.291Z",
        "end_date_fact": "2024-02-01T11:49:10.291Z",
    }
    result.append(data)
    response = client.post("/api/v1/idp/", data=data)
    assert response.status_code == HTTPStatus.CREATED, (
        "Если POST-запрос к `/api/v1/idp/` содержит "
        "корректные данные - должен вернуться ответ со статусом 201."
    )
    return result


def create_task(client):
    idp = create_idp(client)
    result = []
    data = {
        "task_name": "string",
        "task_description": "string",
        "task_status": "draft",
        "task_start_date": "2024-02-01T11:37:08.608Z",
        "task_end_date_plan": "2024-02-01T11:37:08.608Z",
        "task_end_date_fact": "2024-02-01T11:37:08.608Z",
        "task_note_employee": "string",
        "task_note_cheif": "string",
        "idp": idp,
    }
    result.append(data)
    response = client.post("/api/v1/task/", data=data)
    assert response.status_code == HTTPStatus.CREATED, (
        "Если POST-запрос к `/api/v1/task/` содержит "
        "корректные данные - должен вернуться ответ со статусом 201."
    )
    return result
