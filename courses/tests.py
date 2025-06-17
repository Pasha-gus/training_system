from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from courses.models import Course, Lesson

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="student@test.ru", password="testpass123", phone="+79991112233", country="Russia"
        )
        self.user.set_password("testpass123")
        self.user.save()

        self.moderator = User.objects.create(
            email="moderator@test.ru", password="modpass123", is_staff=True, phone="+79994445566"
        )
        self.moderator.set_password("modpass123")
        self.moderator.save()

        self.client.force_authenticate(user=self.user)


class CourseViewSetTest(BaseTestCase):
    def test_course_creation(self):
        url = reverse("courses:course-list")
        data = {"name": "Новый курс", "description": "Описание курса", "price": 1000.00}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

    def test_course_update_by_owner(self):
        course = Course.objects.create(name="Тестовый курс", description="Описание", owner=self.user, price=500.00)
        url = reverse("courses:course-detail", args=[course.pk])
        data = {"name": "Обновленное название"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.name, "Обновленное название")


class LessonAPITest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(name="Основной курс", owner=self.user)

    def test_lesson_creation(self):
        url = reverse("courses:lessons_create")
        data = {
            "name": "Новый урок",
            "description": "Описание урока",
            "course": self.course.pk,
            "url": "https://www.youtube.com/",  # Исправленный URL для валидатора
        }
        response = self.client.post(url, data)
        print(response.data)  # Для отладки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_list(self):
        Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user, url="https://www.youtube.com/"  # Исправленный URL
        )
        url = reverse("courses:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class SubscriptionAPITest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(name="Курс для подписки", owner=self.user)

    def test_subscription_flow(self):
        url = reverse("courses:subscription")

        # Создание подписки
        response = self.client.post(url, {"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

        # Удаление подписки
        response = self.client.post(url, {"course": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
