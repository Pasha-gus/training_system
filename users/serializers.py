from rest_framework.serializers import ModelSerializer

from users.models import Payment, User
from courses.serializers import CourseSerializer


class PaymentSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "phone", "country", "avatar")
        extra_kwargs = {
            'password': {'write_only': True}
        }
