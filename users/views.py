from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import date
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product
from courses.models import Course


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.kwargs.get('course_id')
        course = Course.objects.all().get(id=course_id)
        course_name = course.name
        course_price = course.price
        stripe_product_id = create_stripe_product(course_name)
        stripe_price = create_stripe_price(course_price, stripe_product_id)
        strip_session_id, strip_payment_link = create_stripe_session(stripe_price)
        payment.session_id = strip_session_id
        payment.payment_link = strip_payment_link
        payment.payment_amount = course_price
        payment.payment_date = date.today()
        payment.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()


class LoginAPIView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=request.data['email'])
            user.last_login = date.today()
            user.save()
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
