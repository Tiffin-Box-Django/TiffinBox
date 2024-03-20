from faker import Faker
from django.db.utils import IntegrityError
from django.http import HttpResponse
from .models import TBUser, Schedule, Tiffin

from random import choice

fake = Faker()


def insert_fake_data(request):
    businesses = [("foodex", "FoodEX Budget Non-Veg Tiffins", "foodex@foodex.ca", "admin@1234",
                   "https://th.bing.com/th/id/R.35720bbf29a0f0f1d48195bafdbedf7a?rik=1ArMFF%2fGA8AK1g&riu=http%3a%2f%2fshmector.com%2f_ph%2f13%2f188552034.png&ehk=4W3VAJ3Rgszg4unVrkViPToNE%2b15%2bt3SxRm%2b2VYCdIk%3d&risl=&pid=ImgRaw&r=0"),
                  ("hashtag", "Hastag Budget Veg Tiffins", "admin@hashtag.ca", "admin@1234",
                   "https://static.vecteezy.com/system/resources/previews/000/403/516/original/modern-company-logo-design-vector.jpg"),
                  ("kaurs_kitchen", "Kaur's Kitchen Tiffins", "kar@kk.ca", "admin@1234",
                   "https://images.creativemarket.com/0.1.0/ps/7262394/1820/1214/m1/fpnw/wm0/dining-restaurant-logo-design-inspiration-.jpg?1573169154&s=f5468f33601a341466e0fb5dc1da8c4d")]
    for ele in businesses:
        tmp = TBUser(username=ele[0], first_name=ele[1], email=ele[2], password=ele[3], client_type=1,
                     profile_picture=ele[4], shipping_address=fake.address(), is_registered=True)
        try:
            tmp.save()
        except IntegrityError:
            pass

    for idx in range(7):
        profile = fake.simple_profile()
        tmp = TBUser(username=profile["username"], first_name=profile["name"], email=profile["mail"],
                     client_type=0,
                     profile_picture="https://static3.bigstockphoto.com/thumbs/9/1/7/small2/71941423.jpg",
                     shipping_address=profile["address"], is_registered=False)
        tmp.set_password("admin@1234")
        try:
            tmp.save()
        except IntegrityError:
            pass

    for idx in range(1, 6):
        tmp = Schedule(frequency=idx)
        try:
            tmp.save()
        except IntegrityError:
            pass

    for _ in range(5):
        tmp = Tiffin(schedule_id=Schedule.objects.get(id=choice(range(1, 5))),
                     image="https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto/hmuhx7mgytvwcvkb17h6",
                     business_id=TBUser(id=choice(range(1, 4))), tiffin_name=fake.name(),
                     tiffin_description=fake.text(), meal_type=choice(range(3)), calories=choice(range(100, 300)),
                     price=choice(range(50)), free_delivery_eligible=choice([True, False]), avg_rating=choice(range(6)))
        tmp.save()

    return HttpResponse(content={"message": "OK"})
