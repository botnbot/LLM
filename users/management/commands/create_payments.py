from django.core.management.base import BaseCommand
from users.models import Payments, User
from materials.models import Course, Lesson
from django.utils import timezone


class Command(BaseCommand):
    help = "Создаёт примерные платежи для пользователей"

    def handle(self, *args, **kwargs):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        course1 = Course.objects.get(pk=1)
        lesson3 = Lesson.objects.get(pk=3)

        Payments.objects.create(
            user=user1,
            payment_date=timezone.now(),
            paid_course=course1,
            paid_lesson=None,
            payment_amount=15000.00,
            payment_method="bank_transfer",
        )

        Payments.objects.create(
            user=user2,
            payment_date=timezone.now(),
            paid_course=None,
            paid_lesson=lesson3,
            payment_amount=500.00,
            payment_method="cash",
        )

        self.stdout.write(self.style.SUCCESS("Примерные платежи созданы!"))
