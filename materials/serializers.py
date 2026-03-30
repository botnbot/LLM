from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import YouTubeLinkValidator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YouTubeLinkValidator(field="video_link")
        ]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, course=obj).exists()


class LessonDetailSerializer(ModelSerializer):
    count_course_lessons = SerializerMethodField()
    course = CourseSerializer()

    def get_count_course_lessons(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = ["name", "course", "description", "count_course_lessons"]
