from rest_framework.serializers import ModelSerializer

from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Payments, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }


class PaymentsSerializer(ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payments
        fields = "__all__"

    @staticmethod
    def get_paid_item(obj):
        if obj.paid_course:
            return obj.paid_course.name
        if obj.paid_lesson:
            return obj.paid_lesson.name
        return None