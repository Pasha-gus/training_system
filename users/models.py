from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Пароль")

    avatar = models.ImageField(
        upload_to="users/avatar",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите ваш аватар",
    )
    phone = models.CharField(
        max_length=30, verbose_name="Телефон", help_text="Введите ваш номер телефона"
    )
    country = models.CharField(verbose_name="Страна", help_text="Введите вашу страну")

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("can_blocking_users", "Can blocking users")]

    def __str__(self):
        return self.email
