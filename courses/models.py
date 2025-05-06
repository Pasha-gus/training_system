from django.db import models


class Course(models.Model):

    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/preview_course",
        verbose_name="Превью курса",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):

    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(
        upload_to="materials/preview_lesson",
        verbose_name="Превью урока",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор урока"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
