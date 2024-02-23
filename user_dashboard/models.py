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

class Tiffin(models.Model):
    MEAL = [(0, 'VEG'), (1, 'NON-VEG'), (2, 'VEGAN')]
    RATING = [1, 2, 3, 4, 5]
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    business_id = models.ForeignKey(TBUser, on_delete=models.CASCADE)
    tiffin_name = models.CharField(max_length=50)
    tiffin_description = models.TextField()
    image = models.TextField()
    meal_type = models.IntegerField(choices=MEAL, default=0)
    calories = models.IntegerField()
    price = models.DecimalField(max_digits=4)
    avg_rating = models.IntegerField(choices=RATING)
    free_delivery_eligible = models.BooleanField(default=True)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.tiffin_name