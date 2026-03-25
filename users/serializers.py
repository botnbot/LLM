from rest_framework.serializers import ModelSerializer

from materials.models import Course
from users.models import Payments, User


class UserSerializer(ModelSerializer):
    """Полный сериализатор (для создания/редактирования)"""

    class Meta:
        model = User
        exclude = ["is_staff", "is_superuser", "groups", "user_permissions"]


class UserProfileSerializer(ModelSerializer):
    """Ограниченный сериализатор (для просмотра профиля)"""

    class Meta:
        model = User
        fields = ["id", "email", "avatar", "phone", "city"]


class PaymentsSerializer(ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class CourseShortSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name"]
