from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Payments, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "avatar", "phone", "city")
        extra_kwargs = {"password": {"write_only": True}}


class PaymentsSerializer(ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    paid_course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="paid_course",
        write_only=True,
        required=False,
    )

    paid_lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        source="paid_lesson",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Payments
        fields = [
            "id", "payment_date",
            "paid_course", "paid_lesson",
            "payment_amount", "payment_method"
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"
