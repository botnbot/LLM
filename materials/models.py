from django.db import models
from django.db.models import CASCADE


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    preview = models.ImageField(upload_to="course_previews/", null=True, blank=True)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to="course_previews/", null=True, blank=True)
    video_link = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
         return self.name

