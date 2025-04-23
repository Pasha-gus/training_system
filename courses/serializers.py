from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons_data = SerializerMethodField()

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    def get_lessons_data(self, course):
        return [lessons.name for lessons in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = ("id", "name", "description", "count_lessons", "lessons_data")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
