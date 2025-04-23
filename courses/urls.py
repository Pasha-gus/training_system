from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig

from .views import (CourseViewSet, LessonCreateApiView, LessonDestroyAPIView, LessonListApiView, LessonRetrieveAPIView,
                    LessonUpdateAPIView)

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(),name="lessons_delete",),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),
]

urlpatterns += router.urls
