from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta, date

from config.settings import EMAIL_HOST_USER
from courses.models import Subscription
from users.models import User


@shared_task
def send_mail_update_course_info(course_id):
    """Рассылает письма на почты подписанных на курс пользователей когда курс обновляется"""

    subscription_course_id = Subscription.objects.filter(course=course_id)
    for subscription in subscription_course_id:
        send_mail(
            "Обновление материалов курса",
            f"Курс '{subscription.course.name}' был обновлен",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False
        )


@shared_task(name='courses.check_last_login')
def check_last_login():
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False, last_login__isnull=False)
    date_delta = timedelta(30)
    for user in users:
        date_block = date.today() - date_delta
        if user.last_login <= date_block:
            print('Блокировка пользователя')
            user.is_active = False
            user.save()
