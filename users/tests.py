from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.another_user = User.objects.create_user(
            email="another@example.com", password="password123"
        )

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_retrieve", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_guest_cannot_access_user(self):
        url = reverse("users:users_retrieve", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_access_other_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_retrieve", args=[self.another_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_user_can_update_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_update", args=[self.user.id])
        response = self.client.patch(url, {"email": "new@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new@example.com")

    def test_user_cannot_update_other(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_update", args=[self.another_user.id])
        response = self.client.patch(url, {"city": "Moscow"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_delete", args=[self.another_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users_delete", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)