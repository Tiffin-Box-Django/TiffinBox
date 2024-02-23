from django.db import models
from django.contrib.auth.models import User


class TBUser(User):
    CLIENT_TYPE = [
        (0, 'User'),
        (1, 'Business')]

    profile_picture = models.TextField()
    phone_number = models.CharField(max_length=10)
    client_type = models.IntegerField(choices=CLIENT_TYPE, default=0)
    is_registered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=200)

    class Meta:
        verbose_name = "TBUser"


class TiffinItemList(models.Model):
    name = models.CharField(max_length=200),
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    choices = [
        (1, 'One Day Trial'),
        (2, 'Daily'),
        (3, 'Weekly'),
        (4, 'Monthly')
    ]
    frequency = models.IntegerField(choices=choices)

    def __str__(self):
        return str(self.frequency)
