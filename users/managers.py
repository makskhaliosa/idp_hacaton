from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    """Менеджер для User."""

    use_in_migrations = True

    def _create_user(
        self,
        email,
        first_name,
        last_name,
        position,
        department,
        password,
        **extra_fields
    ):
        """
        Создает и сохраняет пользователя.

        Добавляет указанный адрес электронной почты,
        другие необходимые параметры и пароль.
        """
        if not email:
            raise ValueError("Нужно указать почту.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            position=position,
            department=department,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email,
        first_name,
        last_name,
        position,
        department,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(
            email,
            first_name,
            last_name,
            position,
            department,
            password,
            **extra_fields
        )

    def create_superuser(
        self,
        email,
        first_name="-empty-",
        last_name="-empty-",
        position=None,
        department=None,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Супер пользователь должен быть is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Супер пользователь должен быть is_superuser=True."
            )
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Супер пользователь должен быть is_admin=True.")

        return self._create_user(
            email,
            first_name,
            last_name,
            position,
            department,
            password,
            **extra_fields
        )
