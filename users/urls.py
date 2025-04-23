from django.urls import path

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentDestroyAPIView, PaymentListAPIView, PaymentRetrieveAPIView,
                         PaymentUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_retrieve"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path(
        "payment/<int:pk>/delete/",
        PaymentDestroyAPIView.as_view(),
        name="payment_delete",
    ),
    path(
        "payment/<int:pk>/update/",
        PaymentUpdateAPIView.as_view(),
        name="payment_update",
    ),
]
