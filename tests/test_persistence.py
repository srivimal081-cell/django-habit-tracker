from django.test import TestCase
from Habit.models import User, Habit, AuthToken

class PersistenceTest(TestCase):

    def test_data_saved(self):
        user = User.objects.create(username="testuser")
        Habit.objects.create(
    habit_name="Read",
    description="Book",
    frequency="Daily",
    start_date="2026-04-01",
    user=user
)
        self.assertEqual(Habit.objects.count(), 1)