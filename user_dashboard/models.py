from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


class Orders(models.Model):
    payment_types = [(0, "Credit Card"), (1, "Debit Card"), (2, "Cash"), (3, "Interac")]
    order_status_types = [(0, "Delivered"), (1, "Order Placed"), (2, "Shipped"), (3, "Cancelled")]
    user_id = models.ForeignKey(TBUser, on_delete=models.CASCADE)
    total_price = models.FloatField()
    shipping_address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    payment_method = models.IntegerField(choices=payment_types, default=0)
    status = models.IntegerField(choices=order_status_types, default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)


class TiffinContents(models.Model):
    tiffin = models.ForeignKey(Tiffin, on_delete=models.CASCADE)
    tiffinitem = models.ForeignKey(TiffinItemList, on_delete=models.CASCADE)
    tiffinitem_description = models.TextField()
    quantity = models.IntegerField()
    quantity_metric = models.CharField(max_length=50)

    def __str__(self):
        return f"Tiffin Name: {self.tiffin.tiffin_name}, Tiffin Item: {self.tiffinitem.name}"
