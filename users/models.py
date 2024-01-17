from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uid = models.IntegerField(primary_key=True, verbose_name="user_id")
    first_name = models.CharField(
        verbose_name="first_name", blank=False, max_length=100
    )
    last_name = models.CharField(
        verbose_name="last_name", blank=False, db_index=True, max_length=100
    )
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    position = models.CharField(verbose_name="position", max_length=255)
    chief = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        verbose_name="chief",
        related_name="subordinates",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"
