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


from rest_framework import serializers


class PaymentsSerializer(ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    payment_link = serializers.URLField(read_only=True)

    paid_course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="paid_course",
        write_only=True,
        required=False,
        label="ID курса"
    )

    paid_lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(),
        source="paid_lesson",
        write_only=True,
        required=False,
        label="ID урока"
    )

    def validate(self, data):
        paid_course = data.get("paid_course")
        paid_lesson = data.get("paid_lesson")

        if not paid_course and not paid_lesson:
            raise serializers.ValidationError("Нужно указать курс или урок")

        if paid_course and paid_lesson:
            raise serializers.ValidationError("Можно указать только курс или урок")

        return data

    class Meta:
        model = Payments
        fields = [
            "id",
            "user",
            "payment_date",
            "paid_course_id",
            "paid_lesson_id",
            "paid_course",
            "paid_lesson",
            "payment_method"
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"
