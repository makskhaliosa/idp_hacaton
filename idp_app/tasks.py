import logging

from celery import shared_task

from .models import IDP, Task

logger = logging.getLogger(__name__)


@shared_task(name="change_idp_status")
def change_idp_status(idp_id: str, status: str):
    """Меняет статус ИПР по его id."""
    try:
        logger.info(f"Changing idp {idp_id}")
        idp_obj = IDP.objects.get(idp_id=idp_id)
        idp_obj.status = status
        idp_obj.save()
    except IDP.DoesNotExist:
        logger.error(f"Idp obj does not exists {idp_id}")


@shared_task(name="change_task_status")
def change_task_status(task_id: int, status: str):
    """Меняет статус задачи по ее id."""
    try:
        logger.info(f"Changing task {task_id}")
        task_obj = Task.objects.get(task_id=task_id)
        task_obj.task_status = status
        task_obj.save()
    except Task.DoesNotExist:
        logger.error(f"Task obj does not exists {task_id}")
