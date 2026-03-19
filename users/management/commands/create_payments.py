from datetime import datetime

from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    """"Создать тестовых пользователей, курсы, уроки и платежи"""

    def handle(self, *args, **kwargs):
        # --- Пользователь ---
        user, created_user = User.objects.get_or_create(
            email="testuser@example.com",
            defaults={"password": "123456"}
        )
        if created_user:
            self.stdout.write(self.style.SUCCESS(f"Пользователь {user.email} создан"))
        else:
            self.stdout.write(self.style.WARNING(f"Пользователь {user.email} уже существует"))

        # --- Курс ---
        course, created_course = Course.objects.get_or_create(
            name="Тестовый курс",
            defaults={"description": "Описание тестового курса"}
        )
        if created_course:
            self.stdout.write(self.style.SUCCESS(f"Курс '{course.name}' создан"))
        else:
            self.stdout.write(self.style.WARNING(f"Курс '{course.name}' уже существует"))

        # --- Урок ---
        lesson, created_lesson = Lesson.objects.get_or_create(
            name="Тестовый урок",
            course=course,
            defaults={"description": "Описание тестового урока"}
        )
        if created_lesson:
            self.stdout.write(self.style.SUCCESS(f"Урок '{lesson.name}' создан"))
        else:
            self.stdout.write(self.style.WARNING(f"Урок '{lesson.name}' уже существует"))

        # --- Платежи ---
        payments_data = [
            {"paid_course": course, "paid_lesson": lesson, "payment_amount": 1000, "payment_method": "cash"},
            {"paid_course": course, "paid_lesson": lesson, "payment_amount": 2000, "payment_method": "bank_transfer"},
        ]

        for data in payments_data:
            payment = Payments.objects.create(
                user=user,
                payment_date=datetime.now(),
                **data
            )
            self.stdout.write(self.style.SUCCESS(
                f"Платеж {payment.id} создан: {data['payment_amount']} руб, {data['payment_method']}"
            ))

        self.stdout.write(self.style.SUCCESS("Все тестовые данные созданы!"))