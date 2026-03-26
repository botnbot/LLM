from django.db import models
from django.db.models import CASCADE
from rest_framework.exceptions import ValidationError


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    preview = models.ImageField(upload_to="course_previews/", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=CASCADE, related_name="lessons")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    preview = models.ImageField(upload_to="course_previews/", null=True, blank=True)
    video_link = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def clean(self):
        if self.paid_course and self.paid_lesson:
            raise ValidationError("Нельзя указать одновременно курс и урок")
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError("Нужно указать курс или урок")

    def __str__(self):
        return self.name
