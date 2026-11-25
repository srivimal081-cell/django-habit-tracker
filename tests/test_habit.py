from django.test import TestCase, Client
from Habit.models import User, Habit, AuthToken   

class HabitTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="testuser")
        self.token = AuthToken.objects.create(user=self.user, token="12345")

   
    def test_create_habit_valid(self):

        response = self.client.post(
            "/api/habit/",
            data={
                "habit_name": "Gym",
                "description": "Workout",
                "frequency": "Daily",
                "start_date": "2026-04-01"
            },
            HTTP_AUTHORIZATION="12345"
        )

        self.assertEqual(response.status_code, 200)

   
    def test_create_habit_invalid(self):

        response = self.client.post(
            "/api/habit/",
            data={
                "habit_name": "Gym"
            },
            HTTP_AUTHORIZATION="12345"
        )

        self.assertEqual(response.status_code, 400)

    
    def test_create_habit_invalid_token(self):

        response = self.client.post(
            "/api/habit/",
            data={
                "habit_name": "Gym",
                "description": "Workout",
                "frequency": "Daily",
                "start_date": "2026-04-01"
            },
            HTTP_AUTHORIZATION="wrongtoken"
        )

        self.assertEqual(response.status_code, 401)

  
    def test_search_habit(self):

        Habit.objects.create(
            habit_name="Gym",
            description="Workout",
            frequency="Daily",
            start_date="2026-04-01",
            user=self.user
        )

        response = self.client.get(
            "/api/habit/search/?q=Gym",
            HTTP_AUTHORIZATION="12345"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gym")

    def test_search_invalid(self):

        response = self.client.get(
            "/api/habit/search/?q=XYZ",
            HTTP_AUTHORIZATION="12345"
        )

        self.assertEqual(response.status_code, 200)