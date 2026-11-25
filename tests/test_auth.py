from django.test import TestCase, Client
from Habit.models import User, Habit, AuthToken

class AuthTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="testuser")
        self.token = AuthToken.objects.create(user=self.user, token="12345")

    def test_valid_token(self):
        response = self.client.get(
            "/api/habit/all/",
            HTTP_AUTHORIZATION="12345"
        )
        self.assertNotEqual(response.status_code, 401)

    def test_invalid_token(self):
        response = self.client.get(
            "/api/habit/all/",
            HTTP_AUTHORIZATION="wrong"
        )
        self.assertEqual(response.status_code, 401)

    def test_no_token(self):
        response = self.client.get("/api/habit/all/")
        self.assertEqual(response.status_code, 401)