from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class TBUser(AbstractUser):
    CLIENT_TYPE = [
        (0, 'User'),
        (1, 'Business')]

    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    phone_number = models.CharField(max_length=10, blank=True)
    client_type = models.IntegerField(choices=CLIENT_TYPE, default=0)
    is_registered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "TBUser"

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + str(self.client_type)


class TiffinItemList(models.Model):
    name = models.CharField(max_length=200)
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
        return dict(self.choices)[self.frequency]

    def enum(self):
        return dict(self.choices)[self.frequency]


class Tiffin(models.Model):
    MEAL = [(0, 'VEG'), (1, 'NON-VEG'), (2, 'VEGAN')]

    schedule_id = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING)
    business_id = models.ForeignKey(TBUser, on_delete=models.CASCADE, limit_choices_to={"client_type": 1})
    tiffin_name = models.CharField(max_length=50)
    tiffin_description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    meal_type = models.IntegerField(choices=MEAL, blank=True)
    calories = models.IntegerField(blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, blank=True)
    free_delivery_eligible = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tiffin_name + " " + str(self.meal_type) + " " + str(self.price)


class Order(models.Model):
    PAYMENT_TYPES = [(0, "Credit Card"), (1, "Debit Card"), (2, "Cash"), (3, "Interac")]
    ORDER_STATUS = [(0, "Delivered"), (1, "Order Placed"), (2, "Shipped"), (3, "Cancelled")]

    user_id = models.ForeignKey(TBUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=4, decimal_places=2)
    shipping_address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    payment_method = models.IntegerField(choices=PAYMENT_TYPES, default=0)
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id) + " " + str(self.status) + " " + str(self.payment_method) + " " + str(self.shipping_address)


class TiffinContent(models.Model):
    tiffin = models.ForeignKey(Tiffin, on_delete=models.CASCADE)
    tiffinitem = models.ForeignKey(TiffinItemList, on_delete=models.CASCADE)
    tiffinitem_description = models.TextField(blank=True)
    quantity = models.IntegerField()
    quantity_metric = models.CharField(max_length=50)

    def __str__(self):
        return self.tiffinitem.name + ", " + str(self.quantity) + str(self.quantity_metric)


class Testimonial(models.Model):
    user = models.ForeignKey(TBUser, on_delete=models.DO_NOTHING)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " " + self.comment


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    tiffin_id = models.ForeignKey(Tiffin, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=False)


class Review(models.Model):
    RATINGS = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    user = models.ForeignKey(TBUser, on_delete=models.DO_NOTHING)
    tiffin = models.ForeignKey(Tiffin, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(choices=RATINGS)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + str(self.rating) + " " + self.comment
