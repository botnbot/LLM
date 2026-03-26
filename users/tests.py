from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="llm_user@mail.ru")
        self.admin = User.objects.create_superuser(email="llm_admin@mail.ru")

        self.course = Course.objects.create(name="1", description="Описание1")
        self.lesson1 = Lesson.objects.create(
            name="математика", course=self.course, description="Описание11"
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-detail", args=(self.lesson1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson1.name)

    def test_lesson_create(self):
        url = reverse("materials:lesson-list")
        data = {
            "name": "химия",
            "course": self.course.id,
            "description": "Test description",
            "video_link": "https://youtube.com/video",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson-detail", args=(self.lesson1.pk,))
        response = self.client.patch(url)
        data = {"name": "химия"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "химия")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-detail", args=(self.lesson1.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(
            url,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
