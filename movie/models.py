from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.TextField()
    password = models.CharField(max_length=200)
    email = models.TextField()
    phone = models.TextField()
    name = models.CharField(max_length=200)

    test = models.TextField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user_id