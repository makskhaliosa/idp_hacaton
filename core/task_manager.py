import json
import logging
from datetime import datetime, timedelta

from django_celery_beat.models import ClockedSchedule, PeriodicTask

from .choices import IdpStatuses, TaskStatuses

logger = logging.getLogger(__name__)


def set_idp_status_two_weeks(idp_obj):
    """Создает задачу для смены статуса ИПР на TWO_WEEKS."""
    target_date = idp_obj.end_date_plan
    two_weeks = target_date - timedelta(weeks=2.0)
    schedule = ClockedSchedule.objects.create(clocked_time=two_weeks)
    task_name = f"idp_two_weeks_{idp_obj.idp_id}"
    task_target = "change_idp_status"

    try:
        task = PeriodicTask.objects.get(name=task_name)
    except PeriodicTask.DoesNotExist:
        task = PeriodicTask.objects.create(
            clocked=schedule,
            one_off=True,
            name=task_name,
            task=task_target,
            kwargs=json.dumps(
                {
                    "idp_id": str(idp_obj.idp_id),
                    "status": IdpStatuses.TWO_WEEKS,
                }
            ),
        )
        logger.info(f"created task {task_name}")
        return task

    task.clocked = schedule
    task.enabled = True
    task.task = task_target
    task.save()
    logger.info(f"updated task {task_name}")
    return task


def set_idp_status_overdue(idp_obj):
    """Создает задачу для смены статуса ИПР на OVERDUE."""
    target_date = idp_obj.end_date_plan
    schedule = ClockedSchedule.objects.create(clocked_time=target_date)
    task_name = f"idp_overdue_{idp_obj.idp_id}"
    task_target = "change_idp_status"

    try:
        task = PeriodicTask.objects.get(name=task_name)
    except PeriodicTask.DoesNotExist:
        task = PeriodicTask.objects.create(
            clocked=schedule,
            one_off=True,
            name=task_name,
            task=task_target,
            kwargs=json.dumps(
                {"idp_id": str(idp_obj.idp_id), "status": IdpStatuses.OVERDUE}
            ),
        )
        logger.info(f"created task {task_name}")
        return task

    task.clocked = schedule
    task.enabled = True
    task.task = task_target
    task.save()
    logger.info(f"updated task {task_name}")
    return task


def set_task_status_two_weeks(task_obj):
    """Создает задачу для смены статуса задачи на TWO_WEEKS."""
    target_date = task_obj.task_end_date_plan
    two_weeks = target_date - timedelta(weeks=2.0)
    schedule = ClockedSchedule.objects.create(clocked_time=two_weeks)
    task_name = f"task_two_weeks_{task_obj.task_id}"
    task_target = "change_task_status"

    try:
        task = PeriodicTask.objects.get(name=task_name)
    except PeriodicTask.DoesNotExist:
        task = PeriodicTask.objects.create(
            clocked=schedule,
            one_off=True,
            name=task_name,
            task=task_target,
            kwargs=json.dumps(
                {"task_id": task_obj.task_id, "status": TaskStatuses.TWO_WEEKS}
            ),
        )
        logger.info(f"created task {task_name}")
        return task

    task.clocked = schedule
    task.enabled = True
    task.task = task_target
    task.save()
    logger.info(f"updated task {task_name}")
    return task


def set_task_status_overdue(task_obj):
    """Создает задачу для смены статуса задачи на OVERDUE."""
    target_date = task_obj.task_end_date_plan
    schedule = ClockedSchedule.objects.create(clocked_time=target_date)
    task_name = f"task_overdue_{task_obj.task_id}"
    task_target = "change_task_status"

    try:
        task = PeriodicTask.objects.get(name=task_name)
    except PeriodicTask.DoesNotExist:
        task = PeriodicTask.objects.create(
            clocked=schedule,
            one_off=True,
            name=task_name,
            task=task_target,
            kwargs=json.dumps(
                {"task_id": task_obj.task_id, "status": TaskStatuses.OVERDUE}
            ),
        )
        logger.info(f"created task {task_name}")
        return task

    task.clocked = schedule
    task.enabled = True
    task.task = task_target
    task.save()
    logger.info(f"updated task {task_name}")
    return task


def define_idp_task(idp_obj):
    """Определяет логику создания задач на смену статуса для объектов IDP."""
    if idp_obj.status in (IdpStatuses.ACTIVE, IdpStatuses.TWO_WEEKS):
        logger.info("Defining task")
        tz = idp_obj.end_date_plan
        if tz - datetime.now().astimezone(None) > timedelta(weeks=2.0):
            set_idp_status_two_weeks(idp_obj)
        else:
            set_idp_status_overdue(idp_obj)

    elif idp_obj.status in (
        IdpStatuses.CANCELLED,
        IdpStatuses.COMPLETED_APPROVAL,
    ):
        two_weeks_task = f"idp_two_week_{idp_obj.idp_id}"
        overdue_task = f"idp_overdue_{idp_obj.idp_id}"
        logger.info(f"Cancelling task {idp_obj.idp_id}")
        task_list = [two_weeks_task, overdue_task]

        current_task = None
        for task_name in task_list:
            try:
                current_task = PeriodicTask.objects.get(name=task_name)
            except PeriodicTask.DoesNotExist:
                continue
            else:
                break
        if current_task is not None:
            current_task.enabled = False
            current_task.save()
            logger.info(f"Cancelled task {current_task.name}")


def define_task_obj_task(task_obj):
    """Определяет логику создания задач на смену статуса для объектов Task."""
    if task_obj.task_status in (TaskStatuses.ACTIVE, TaskStatuses.TWO_WEEKS):
        logger.info("Defining task")

        tz = task_obj.task_end_date_plan
        if tz - datetime.now().astimezone(None) > timedelta(weeks=2.0):
            set_task_status_two_weeks(task_obj)
        else:
            set_task_status_overdue(task_obj)

    elif task_obj.task_status in (
        TaskStatuses.CANCELLED,
        TaskStatuses.COMPLETED_APPROVAL,
    ):
        two_weeks_task = f"task_two_week_{task_obj.task_id}"
        overdue_task = f"task_overdue_{task_obj.task_id}"
        logger.info(f"Cancelling task {task_obj.task_id}")
        task_list = [two_weeks_task, overdue_task]

        current_task = None
        for task_name in task_list:
            try:
                current_task = PeriodicTask.objects.get(name=task_name)
            except PeriodicTask.DoesNotExist:
                continue
            else:
                break
        if current_task is not None:
            current_task.enabled = False
            current_task.save()
            logger.info(f"Cancelled task {current_task.name}")
