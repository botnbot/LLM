from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):

    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, course):
        return course.lessons.count()


class LessonDetailSerializer(ModelSerializer):
    count_course_lessons = SerializerMethodField()
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_count_course_lessons(self, lesson):
        return lesson.course.lessons.count()

    class Meta:
        model = Lesson
        fields = ["id", "name", "course", "description", "video_link", "count_course_lessons"]