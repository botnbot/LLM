from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from config import settings
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
        ("stripe", "Stripe"),
        ("cash", "Наличные"),
    ]

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
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
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Сумма оплаты",
        help_text="Введите сумму оплаты",

    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )
    payment_link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL,
                             verbose_name='пользователь',
                             help_text='Укажите пользователя')

    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Ожидание"),
            ("paid", "Оплачено"),
            ("canceled", "Отменено"),
        ],
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


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        item = self.get_paid_item()
        item_name = item.name if item else "Нет"
        user_email = self.user.email if self.user else "Нет пользователя"
        return f"{user_email} — {item_name} — {self.payment_amount} руб. ({self.payment_method})"

    class Meta:
        verbose_name='Платеж'
        verbose_name_plural='Платежи'

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
