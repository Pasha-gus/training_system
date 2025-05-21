from django.contrib import admin

from courses.models import Course, Lesson

# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "course")
    list_filter = ("name",)
    search_fields = ("course",)
