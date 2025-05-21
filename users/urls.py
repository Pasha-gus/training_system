from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    UserCreateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("payment/course/<int:course_id>/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/list/", PaymentListAPIView.as_view(), name="payment_list"),

    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]
