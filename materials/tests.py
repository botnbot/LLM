from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription, User


class LessonCRUDTests(APITestCase):

    def setUp(self):
        self.moderator_group, _ = Group.objects.get_or_create(name="Moderators")

        self.moderator = User.objects.create_user(
            email="mod@example.com", password="password123"
        )
        self.moderator.groups.add(self.moderator_group)

        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )

        self.course1 = Course.objects.create(name="Курс 1", owner=self.moderator)
        self.course2 = Course.objects.create(name="Курс 2", owner=self.moderator)

        self.lesson1 = Lesson.objects.create(
            name="Урок 1", course=self.course1, owner=self.moderator
        )
        self.lesson2 = Lesson.objects.create(
            name="Урок 2", course=self.course1, owner=self.moderator
        )

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-detail", args=[self.lesson1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count_course_lessons", response.data)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-list")
        data = {"name": "Урок 3", "course": self.course2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-detail", args=[self.lesson1.id])
        data = {"name": "Урок 1 обновлён"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.name, "Урок 1 обновлён")

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-detail", args=[self.lesson2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 1)


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.course = Course.objects.create(name="Курс 1")

    def test_add_subscription(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )