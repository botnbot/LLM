from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


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

    def test_unauthorized_cannot_create_lesson(self):
        url = reverse("materials:lessons-list")
        response = self.client.post(url, {"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_update_not_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons-detail", args=[self.lesson1.id])
        response = self.client.patch(url, {"name": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-detail", args=[self.lesson1.id])
        response = self.client.patch(url, {"name": "Owner update"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_delete_any(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons-detail", args=[self.lesson1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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

    def test_double_subscription_toggle(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscriptions")

        # добавили
        self.client.post(url, {"course_id": self.course.id})
        # удалили
        self.client.post(url, {"course_id": self.course.id})
        # снова добавили
        response = self.client.post(url, {"course_id": self.course.id})

        self.assertEqual(response.status_code, 201)

    def test_guest_cannot_subscribe(self):
        url = reverse("materials:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_invalid_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscriptions")
        response = self.client.post(url, {"course_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_without_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscriptions")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CourseTests(APITestCase):

    def setUp(self):
        self.moderator_group, _ = Group.objects.get_or_create(name="Moderators")
        self.moderator = User.objects.create_user(email="mod@example.com", password="password123")
        self.moderator.groups.add(self.moderator_group)

        self.user = User.objects.create_user(email="user@example.com", password="password123")

        self.course = Course.objects.create(name="Курс 1", owner=self.moderator)

    def test_list_courses(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:courses_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_create_course_authorized(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:courses_create")
        data = {"name": "Новый курс"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.filter(name="Новый курс").count(), 1)

    def test_create_course_unauthorized(self):
        url = reverse("materials:courses_create")
        data = {"name": "Новый курс"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_course_owner(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:courses_update", args=[self.course.id])
        data = {"name": "Обновлённый курс"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Обновлённый курс")

    def test_delete_course_not_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:courses_delete", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
