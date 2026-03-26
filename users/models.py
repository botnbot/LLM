from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from materials import serializers
from materials.models import Course, Lesson
from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    city = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("bank_transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
    )
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    def get_paid_item(self):
        """Возвращает оплаченный курс или урок"""
        if self.paid_course:
            return self.paid_course
        if self.paid_lesson:
            return self.paid_lesson
        return None

    def clean(self):
        if self.paid_course and self.paid_lesson:
            raise ValidationError("Нельзя оплатить курс и урок одновременно")

        if not self.paid_course and not self.paid_lesson:
            raise ValidationError("Нужно выбрать курс или урок")

    def __str__(self):
        item = self.get_paid_item()
        item_name = item.name if item else "Нет"
        return f"{self.user.email} — {item_name} — {self.payment_amount} руб. ({self.payment_method})"
