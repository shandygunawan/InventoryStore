import json
from django.urls import include, path, reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase

from accounts.models import User


class UserTest(APITestCase, URLPatternsTestCase):

    urlpatterns = [
        path('auth/', include('accounts.urls'))
    ]

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="test"
        )

        self.admin = User.objects.create_superuser(
            username="testadmin1",
            password="admin"
        )

    def test_login(self):
        url = reverse('account-login')
        data = {
            "username": "testadmin1",
            "password": "admin"
        }
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['success'], True)
        self.assertTrue('access' in response_data)

    def test_registration(self):
        url = reverse('account-registration')
        data = {
            "username": "testuser2",
            "password": "test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)