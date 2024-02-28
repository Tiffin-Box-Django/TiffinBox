from django.contrib.auth.models import User
from django.db import models


class Business(User):
    registered_enum = [
        (0, 'Not Registered'),
        (1, 'Registered'),
        (2, 'Registration in process')]

    business_name = models.CharField(max_length=200, unique=True, null=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True)
    is_registered = models.IntegerField(choices=registered_enum, null=False, default=0)

    class Meta:
        verbose_name = "Business"

    def __str__(self):
        return f"Business: {self.first_name} {self.last_name} {self.business_name}"
