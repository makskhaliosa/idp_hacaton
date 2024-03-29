import uuid
from datetime import datetime
from typing import Any, Dict, List

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.choices import (
    IdpNoteRelation,
    IdpStatuses,
    NotificationStatuses,
    NotificationTriggers,
    TaskNoteRelation,
    TaskStatuses,
    UserRoles,
)
from core.task_manager import define_idp_task, define_task_obj_task
from core.utils import default_end_date_plan, find_differencies
from idp.settings import INCLUDE_CELERY

User = get_user_model()


class IDP(models.Model):
    """Таблица ИПР."""

    idp_id = models.UUIDField(
        primary_key=True,
        verbose_name="idp_id",
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name="name",
        max_length=100,
    )
    target = models.TextField(
        verbose_name="target", max_length=255, blank=True, null=True
    )
    status = models.CharField(
        verbose_name="status",
        max_length=255,
        choices=IdpStatuses,
        default=IdpStatuses.DRAFT,
    )
    start_date = models.DateTimeField(
        verbose_name="start_date", default=datetime.now, blank=True, null=True
    )
    end_date_plan = models.DateTimeField(
        verbose_name="end_date_plan",
        default=default_end_date_plan,
        blank=True,
        null=True,
    )
    end_date_fact = models.DateTimeField(
        verbose_name="end_date_fact", blank=True, null=True
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="idps"
    )
    notifications = models.ManyToManyField(
        "Notification",
        through="IdpNotification",
        verbose_name="notifications",
        blank=True,
    )

    class Meta:
        ordering = ("name", "start_date")
        verbose_name = "IDP"
        verbose_name_plural = "IDPs"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        try:
            _original = IDP.objects.get(idp_id=self.pk)
            differencies = find_differencies(_original, self)
            super().save(*args, **kwargs)
            self._handle_differencies(differencies)
        except self.DoesNotExist:
            super().save(*args, **kwargs)
            trigger = IdpNoteRelation.get(self.status)
            if trigger is not None:
                self._create_notification(trigger)
            self._change_tasks_status(self.status)
        if INCLUDE_CELERY:
            define_idp_task(self)

    def _create_notification(self, trigger: Dict[str, Any]):
        try:
            note = Notification.objects.get(trigger=trigger.get("note"))
            messages = trigger.get("message")
            receivers_messages = self._get_receiver_and_message(
                users=trigger.get("receiver", [UserRoles.employee]),
                messages=messages,
            )
            for receiver, message in receivers_messages.items():
                final_message = f"{message} {self.get_absolute_url()}"
                IdpNotification.objects.create(
                    notification=note,
                    idp=self,
                    receiver=receiver,
                    message=final_message,
                )
        except Notification.DoesNotExist:
            return None

    def _handle_differencies(self, differencies: Dict[str, Any]):
        if "status" in differencies:
            trigger = IdpNoteRelation.get(self.status)
            if trigger:
                self._create_notification(trigger)
            self._change_tasks_status(self.status)
        else:
            trigger = IdpNoteRelation.get("updated")
            self._create_notification(trigger)

    def _get_receiver_and_message(
        self, users: List[str], messages: Dict[str, str]
    ) -> Dict[User, str]:
        """
        Принимает список ролей и словарь с сообщениями для ролей.

        Возвращает словарь, где ключ - получатель, а значение - сообщение.
        """
        receivers = {
            UserRoles.employee: self.employee,
            UserRoles.chief: self.employee.chief,
        }
        return {receivers.get(user): messages.get(user) for user in users}

    def _change_tasks_status(self, status: str):
        """
        Получает статус ИПР и обновляет статус задач.

        Статус задач полуаем из словаря соответствий статусов.
        """
        statuses = {
            IdpStatuses.ACTIVE: TaskStatuses.ACTIVE_WITH_IDP,
            IdpStatuses.CANCELLED: TaskStatuses.CANCELLED_WITH_IDP,
            IdpStatuses.DRAFT_APPROVAL: TaskStatuses.DRAFT_APPROVAL,
        }
        updated_status = statuses.get(status)
        if updated_status:
            for task in self.tasks.all():
                task.task_status = updated_status
                task.save()

    def get_absolute_url(self):
        return reverse("idp-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    """Таблица для задач."""

    task_id = models.AutoField(primary_key=True, verbose_name="task_id")
    task_name = models.CharField(verbose_name="task_name", max_length=150)
    task_description = models.CharField(
        verbose_name="task_description",
        max_length=10000,
    )
    task_status = models.CharField(
        verbose_name="task_status",
        max_length=40,
        choices=TaskStatuses,
        default=TaskStatuses.DRAFT,
    )
    task_start_date = models.DateTimeField(
        verbose_name="task_start_date",
        default=datetime.now,
    )
    task_end_date_plan = models.DateTimeField(
        verbose_name="task_end_date_plan",
        blank=True,
        null=True,
    )
    task_end_date_fact = models.DateTimeField(
        verbose_name="task_end_date_fact", blank=True, null=True
    )
    task_note_employee = models.CharField(
        verbose_name="task_note_employee",
        max_length=10000,
        blank=True,
        null=True,
    )
    task_note_chief = models.CharField(
        verbose_name="task_note_chief", max_length=10000, blank=True, null=True
    )
    task_note_mentor = models.CharField(
        verbose_name="task_note_mentor",
        max_length=10000,
        blank=True,
        null=True,
    )
    task_mentor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="task_mentor",
        related_name="mentor_tasks",
        blank=True,
        null=True,
    )
    idp = models.ForeignKey(
        IDP, on_delete=models.CASCADE, related_name="tasks", verbose_name="idp"
    )
    notifications = models.ManyToManyField(
        "Notification",
        through="TaskNotification",
        verbose_name="notifications",
        blank=True,
    )

    class Meta:
        ordering = ("task_id",)
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return f"Task №{self.task_id}"

    def save(self, *args, **kwargs):
        try:
            _original = Task.objects.get(task_id=self.pk)
            differencies = find_differencies(_original, self)
            super().save(*args, **kwargs)
            self._handle_differencies(differencies)
        except self.DoesNotExist:
            super().save(*args, **kwargs)
            trigger = TaskNoteRelation.get(self.task_status)
            if trigger is not None:
                self._create_notification(trigger)
        if INCLUDE_CELERY:
            define_task_obj_task(self)

    def _create_notification(self, trigger: Dict[str, Any]):
        try:
            note = Notification.objects.get(trigger=trigger.get("note"))
            messages = trigger.get("message")
            receivers_messages = self._get_receiver_and_message(
                users=trigger.get("receiver", [UserRoles.employee]),
                messages=messages,
            )
            for receiver, message in receivers_messages.items():
                final_message = f"{message} {self.get_absolute_url()}"
                TaskNotification.objects.create(
                    notification=note,
                    task=self,
                    receiver=receiver,
                    message=final_message,
                )
        except Notification.DoesNotExist:
            return None

    def _handle_differencies(self, differencies: Dict[str, Any]):
        if "task_status" in differencies:
            trigger = TaskNoteRelation.get(self.task_status)
            del differencies["task_status"]
            if trigger:
                self._create_notification(trigger)
            if self.task_status == TaskStatuses.CLOSED:
                self._check_other_tasks()
        for field in differencies.keys():
            trigger = TaskNoteRelation.get(field)
            if trigger:
                self._create_notification(trigger)

    def _get_receiver_and_message(
        self, users: List[str], messages: Dict[str, str]
    ) -> Dict[User, str]:
        """
        Принимает список ролей и словарь с сообщениями для ролей.

        Возвращает словарь, где ключ - получатель, а значение - сообщение.
        """
        receivers = {
            UserRoles.employee: self.idp.employee,
            UserRoles.chief: self.idp.employee.chief,
            UserRoles.mentor: self.task_mentor,
        }
        return {receivers.get(user): messages.get(user) for user in users}

    def _check_other_tasks(self):
        all_tasks_done = True
        # проверяем остальные таски на завершенность
        for task in self.idp.tasks.all():
            if not all_tasks_done:
                break
            if task.task_status != TaskStatuses.CLOSED:
                all_tasks_done = False
        if all_tasks_done:
            self.idp.status = IdpStatuses.COMPLETED_APPROVAL
            self.idp.save()

    def get_absolute_url(self):
        return reverse(
            "tasks-detail", kwargs={"pk": self.pk, "idp_id": self.idp.idp_id}
        )


class File(models.Model):
    """Таблица для файлов."""

    file_id = models.AutoField(primary_key=True, verbose_name="file_id")
    file = models.FileField(upload_to="uploads/")
    file_name = models.CharField(
        verbose_name="file_name", max_length=100, default="file"
    )
    file_type = models.CharField(
        verbose_name="file_type", max_length=50, blank=True
    )
    file_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="file_task",
        related_name="task_files",
        default=None,
    )

    class Meta:
        ordering = ("file_id",)
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self) -> str:
        return self.file_name


class Notification(models.Model):
    """Таблица для уведомлений."""

    notice_id = models.AutoField(
        primary_key=True, verbose_name="notification_id"
    )
    trigger = models.CharField(
        verbose_name="notification_trigger",
        choices=NotificationTriggers,
        default=NotificationTriggers.IDP_CREATED,
        max_length=255,
    )
    name = models.CharField(verbose_name="notification_name", max_length=255)
    description = models.TextField(
        verbose_name="notification_description", blank=True, null=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self) -> str:
        return f"{self.name} {self.trigger}"


class TaskNotification(models.Model):
    """Связующая таблица для уведомлений и пользователей, связанных с задачами."""

    tn_id = models.BigAutoField(
        primary_key=True, verbose_name="notification_user_id"
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="notice_tasks",
        verbose_name="notification",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_notices",
        verbose_name="task",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task_notices",
        verbose_name="receiver_of_notice",
        null=True,
    )
    message = models.TextField(
        verbose_name="notification_message", blank=True, null=True
    )
    date = models.DateTimeField(
        verbose_name="notification_sent_datetime", auto_now_add=True
    )
    status = models.CharField(
        verbose_name="notification_status",
        choices=NotificationStatuses,
        max_length=40,
        default=NotificationStatuses.UNREAD,
    )

    def __str__(self) -> str:
        return f"{self.notification} {self.task}"


class IdpNotification(models.Model):
    """Связующая таблица для уведомлений и пользователей, связанных с ипр."""

    in_id = models.BigAutoField(
        primary_key=True, verbose_name="notification_user_id"
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="notice_idps",
        verbose_name="notification",
    )
    idp = models.ForeignKey(
        IDP,
        on_delete=models.CASCADE,
        related_name="idp_notices",
        verbose_name="idp",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="idp_notices",
        verbose_name="receiver_of_notice",
        null=True,
    )
    message = models.TextField(
        verbose_name="notification_message", blank=True, null=True
    )
    date = models.DateTimeField(
        verbose_name="notification_sent_datetime", auto_now_add=True
    )
    status = models.CharField(
        verbose_name="notification_status",
        choices=NotificationStatuses,
        max_length=40,
        default=NotificationStatuses.UNREAD,
    )

    def __str__(self) -> str:
        return f"{self.notification} {self.idp}"
