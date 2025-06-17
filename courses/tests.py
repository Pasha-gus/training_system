from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TransactionTestCase
from django.core.management import call_command

from courses.models import Course, Lesson, Subscription
from users.models import User


class BaseTestCase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('migrate', verbosity=0)

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@test.ru",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)


class CoursesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            description="Описание урока 1",
            course=self.course,
            owner=self.user
        )

    def test_lesson_create(self):
        url = reverse("courses:lessons_create")
        data = {
            "name": "Урок 2",
            "description": "Описание урока 2",
            "course": self.course.pk,
            "url": "http://www.youtube.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse("courses:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Урок 3",
            "description": "Описание урока 3",
            "course": self.course.pk,
            "url": "http://www.youtube.com",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Урок 3")

    def test_lesson_delete(self):
        url = reverse("courses:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("courses:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Урок 1")

    def test_lesson_retrieve(self):
        url = reverse("courses:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Урок 1")


class SubscriptionTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(
            name="Курс 1",
            description="Описание",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            description="Описание",
            course=self.course,
            owner=self.user
        )
        self.subscription = Subscription.objects.create(
            course=self.course,
            user=self.user
        )

    def test_subscription(self):
        url = reverse("courses:subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")
