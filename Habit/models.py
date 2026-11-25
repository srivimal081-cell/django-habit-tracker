from django.contrib.auth.models import User
from django.db import models
import uuid


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()

    def __str__(self):
        return self.habit_name


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)