from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    preview = models.ImageField(upload_to="course_previews/", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name="Создатель",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    preview = models.ImageField(upload_to="lesson_previews/", null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name="Создатель",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return f"{self.name} ({self.course})"
