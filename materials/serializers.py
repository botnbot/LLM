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
        fields = "__all__"

    def get_lessons_count(self, course):
        return course.lessons.count()


class LessonDetailSerializer(ModelSerializer):
    count_course_lessons = SerializerMethodField()
    course = CourseSerializer()

    def get_count_course_lessons(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = ["name", "course", "description", "count_course_lessons"]
