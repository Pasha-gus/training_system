from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson, Subscription
from courses.validators import UrlValidator


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons_data = SerializerMethodField()
    in_subscription = SerializerMethodField()

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    def get_lessons_data(self, course):
        return [lessons.name for lessons in Lesson.objects.filter(course=course)]

    def get_in_subscription(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return Subscription.objects.filter(course=obj, user=user).exists()
        return False

    class Meta:
        model = Course
        fields = ("id", "name", "description", "count_lessons", "lessons_data", "in_subscription")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="url")]


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
