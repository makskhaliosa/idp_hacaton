import uuid
from datetime import datetime
from typing import Any, Dict, List

from django.contrib.auth import get_user_model
from django.db import models

from core.choices import (
    NotificationStatuses,
    NotificationTriggers,
    StatusChoices,
    IdpNoteRelation,
    IdpStatuses,
    TaskNoteRelation,
    TaskStatuses,
)
from core.utils import default_end_date_plan, find_differencies

User = get_user_model()


class IDP(models.Model):
    """IDP table."""

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
    mentor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="mentor",
        related_name="idp",
        blank=True,
        null=True,
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
            if self.status == IdpStatuses.ACTIVE:
                self._activate_tasks()

    def _create_notification(self, trigger: Dict[str, Dict]):
        try:
            note = Notification.objects.get(trigger=trigger.get("note"))
            receivers = self._get_receiver(
                trigger.get("receiver", ["employee"])
            )
            [
                IdpNotification.objects.create(
                    notification=note, idp=self, receiver=receiver
                )
                for receiver in receivers
            ]
        except Notification.DoesNotExist:
            return None

    def _handle_differencies(self, differencies: Dict[str, Any]):
        if "status" in differencies:
            trigger = IdpNoteRelation.get(self.status)
            if trigger:
                self._create_notification(trigger)
            if self.status == IdpStatuses.ACTIVE:
                self._activate_tasks()
            elif self.status == IdpStatuses.CANCELLED:
                self._cancel_tasks()
        else:
            trigger = IdpNoteRelation.get("updated")
            self._create_notification(trigger)

    def _get_receiver(self, users: List[str]) -> List[User]:
        receivers = {"employee": self.employee, "chief": self.employee.chief}
        return [receivers.get(user) for user in users]

    def _activate_tasks(self):
        for task in self.tasks.all():
            task.task_status = TaskStatuses.ACTIVE_WITH_IDP
            task.save()

    def _cancel_tasks(self):
        for task in self.tasks.all():
            task.task_status = TaskStatuses.CANCELLED_WITH_IDP
            task.save()


class Task(models.Model):
    """Tasks table."""

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
    mentor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="mentor",
        related_name="tasks",
        blank=True,
        null=True,
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
    task_note_cheif = models.CharField(
        verbose_name="task_note_cheif", max_length=10000, blank=True, null=True
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

    def _create_notification(self, trigger: Dict[str, Dict]):
        try:
            note = Notification.objects.get(trigger=trigger.get("note"))
            receivers = self._get_receiver(
                trigger.get("receiver", ["employee"])
            )
            [
                TaskNotification.objects.create(
                    notification=note, task=self, receiver=receiver
                )
                for receiver in receivers
            ]
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

    def _get_receiver(self, users: List[str]) -> List[User]:
        receivers = {
            "employee": self.idp.employee,
            "chief": self.idp.employee.chief,
            "mentor": self.task_mentor,
        }
        return [receivers.get(user) for user in users]

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


class File(models.Model):
    """Files table."""

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
    """Notifications table."""

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
    """Link table for task related notifications and users."""

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
    """Link table for idp related notifications and users."""

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
