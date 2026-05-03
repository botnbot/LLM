from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


@shared_task
def send_course_update_email(course_id, user_email, course_name):
    """Отправка email об обновлении курса конкретному пользователю"""
    subject = f'Курс "{course_name}" был обновлен!'
    message = f'''
    Здравствуйте!

    Курс "{course_name}", на который вы подписаны, был обновлен.
    Приглашаем вас ознакомиться с новыми материалами.

    С уважением,
    Команда платформы
    '''

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return f"Email sent to {user_email}"
    except Exception as e:
        return f"Error sending email to {user_email}: {str(e)}"


@shared_task
def notify_course_subscribers(course_id, course_name):
    """Уведомление всех подписчиков курса об обновлении"""
    from users.models import Subscription

    # Получаем всех подписчиков курса
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user')

    if not subscriptions.exists():
        return f"No subscribers for course {course_name}"

    # Отправляем уведомления всем подписчикам
    for subscription in subscriptions:
        send_course_update_email.delay(
            course_id=course_id,
            user_email=subscription.user.email,
            course_name=course_name
        )

    return f"Notifications sent to {subscriptions.count()} subscribers"


@shared_task
def block_inactive_users():
    """
    Блокировка пользователей, которые не заходили более месяца
    """
    User = get_user_model()

    # Вычисляем дату месяц назад
    month_ago = timezone.now() - timedelta(days=30)

    # Находим активных пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    )

    count = inactive_users.count()

    # Блокируем пользователей
    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"User {user.email} has been blocked due to inactivity")

    result_message = f"{count} users have been blocked for inactivity"
    print(result_message)

    return result_message


@shared_task
def test_task():
    """Тестовая задача"""
    print("Celery работает")
    return "Task completed"