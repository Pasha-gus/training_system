from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson


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
    phone = models.CharField(max_length=30, verbose_name="Телефон", help_text="Введите ваш номер телефона")
    country = models.CharField(verbose_name="Страна", help_text="Введите вашу страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD = (
        ("cash", "наличные"),
        ("transfer", "перевод"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    payment_date = models.DateField()
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    payment_amount = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        choices=PAYMENT_METHOD,
        max_length=255,
        default="cash",
        verbose_name="Способ оплаты",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.paid_course} ({self.payment_amount})"
