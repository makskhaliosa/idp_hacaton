import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.itercompat import is_iterable

from .managers import CustomUserManager


class User(AbstractBaseUser):
    """Таблица для сотрудников."""

    uid = models.UUIDField(
        primary_key=True,
        verbose_name="user_id",
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(verbose_name="first_name", max_length=100)
    middle_name = models.CharField(
        verbose_name="middle_name", max_length=100, blank=True
    )
    last_name = models.CharField(verbose_name="last_name", max_length=100)
    email = models.EmailField(
        verbose_name="user_email", max_length=100, db_index=True, unique=True
    )
    position = models.ForeignKey(
        "Position",
        on_delete=models.SET_NULL,
        verbose_name="user_position",
        related_name="users",
        null=True,
    )
    chief = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        verbose_name="chief",
        related_name="subordinates",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name="user_department",
        null=True,
    )
    is_admin = models.BooleanField(verbose_name="user_is_admin", default=False)
    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        verbose_name="active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        verbose_name="superuser status",
        default=False,
        help_text=(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        """
        Return full name.

        The first_name, middle_name if there is one and the last_name,
        with a space in between.
        """
        middle_full_name = (
            f"{self.first_name} {self.middle_name} {self.last_name}"
        )
        full_name = f"{self.first_name} {self.last_name}"
        return middle_full_name if self.middle_name else full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Return True if the user is active and admin or superuser.

        Needs further development for common users.
        """
        # Active superusers have all permissions.
        if self.is_active and (self.is_admin or self.is_superuser):
            return True
        return False

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions.

        If object is passed, check if the user has all required perms for it.
        """
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.

        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and (self.is_admin or self.is_superuser):
            return True
        return False


class Position(models.Model):
    """Таблица с наименованием должностей сотрудников."""

    pos_id = models.AutoField(verbose_name="position_id", primary_key=True)
    name = models.CharField(
        verbose_name="position_name", max_length=255, unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Position"
        verbose_name_plural = "Positions"


class Company(models.Model):
    """Company table."""

    company_id = models.AutoField(
        primary_key=True,
        verbose_name="company_id",
    )
    company_name = models.CharField(
        verbose_name="company_name", max_length=200
    )

    class Meta:
        ordering = ("company_id",)
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.company_name


class Department(models.Model):
    """Department table."""

    dep_id = models.AutoField(primary_key=True, verbose_name="dep_id")
    dep_name = models.CharField(verbose_name="dep_name", max_length=400)
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="company_id",
    )

    class Meta:
        ordering = ("dep_id",)
        verbose_name = "Department"
        verbose_name_plural = "Departmens"

    def __str__(self) -> str:
        return self.dep_name
