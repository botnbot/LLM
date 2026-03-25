from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons", "lessons_count"]

    def get_lessons_count(self, course):
        return course.lessons.count()


class CourseShortSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name"]


class LessonDetailSerializer(ModelSerializer):
    count_course_lessons = SerializerMethodField()
    course = CourseShortSerializer()

    def get_count_course_lessons(self, lesson):
        return lesson.course.lessons.count()

    class Meta:
        model = Lesson
        fields = ["name", "course", "description", "count_course_lessons"]
