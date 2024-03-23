from faker import Faker
from django.db.utils import IntegrityError
from django.http import HttpResponse
from .models import TBUser, Schedule, Tiffin, Review, Testimonial

from random import choice

fake = Faker()


def insert_fake_data(request):
    businesses = [("foodex", "FoodEX Budget Non-Veg Tiffins", "foodex@foodex.ca", "admin@1234",
                   "https://th.bing.com/th/id/R.35720bbf29a0f0f1d48195bafdbedf7a?rik=1ArMFF%2fGA8AK1g&riu=http%3a%2f%2fshmector.com%2f_ph%2f13%2f188552034.png&ehk=4W3VAJ3Rgszg4unVrkViPToNE%2b15%2bt3SxRm%2b2VYCdIk%3d&risl=&pid=ImgRaw&r=0"),
                  ("hashtag", "Hastag Budget Veg Tiffins", "admin@hashtag.ca", "admin@1234",
                   "https://static.vecteezy.com/system/resources/previews/000/403/516/original/modern-company-logo-design-vector.jpg"),
                  ("kaurs_kitchen", "Kaur's Kitchen Tiffins", "kar@kk.ca", "admin@1234",
                   "https://images.creativemarket.com/0.1.0/ps/7262394/1820/1214/m1/fpnw/wm0/dining-restaurant-logo-design-inspiration-.jpg?1573169154&s=f5468f33601a341466e0fb5dc1da8c4d")]
    business_ids = (1, len(businesses))
    for ele in businesses:
        tmp = TBUser(username=ele[0], first_name=ele[1], email=ele[2], client_type=1,
                     profile_picture=ele[4], shipping_address=fake.address(), is_registered=True)
        tmp.set_password("admin@1234")
        try:
            tmp.save()
        except IntegrityError:
            pass

    user_ids = (len(business_ids), len(business_ids) + 7)
    for _ in range(*user_ids):
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

    tiffin_ids = (1, 10)
    for _ in range(*tiffin_ids):
        tmp = Tiffin(schedule_id=Schedule.objects.get(id=choice(range(1, 5))),
                     image="https://res.cloudinary.com/swiggy/image/upload/fl_lossy,f_auto,q_auto/hmuhx7mgytvwcvkb17h6",
                     business_id=TBUser.objects.get(id=choice(range(*business_ids))), tiffin_name=fake.name(),
                     tiffin_description=fake.text(), meal_type=choice(range(3)), calories=choice(range(100, 300)),
                     price=choice(range(10, 50)), free_delivery_eligible=choice([True, False]),
                     avg_rating=choice(range(1, 6)))
        tmp.save()

    # add reviews
    # select users
    for user_id in range(*user_ids):
        # select tiffins
        for tiffin_id in range(*tiffin_ids):
            tmp = Review(user=TBUser.objects.get(id=user_id),
                         tiffin=Tiffin.objects.get(id=tiffin_id),
                         rating=choice(range(1, 6)),
                         comment=fake.text()[:150])
            tmp.save()

    # testimonials
    testimonial_text = ["Absolutely love the convenience and deliciousness of TiffinBox! As a busy professional, having healthy and tasty meals delivered to my doorstep has been a game-changer. The variety of options keeps me excited for each delivery, and the freshness of the ingredients shines through in every bite. Highly recommend!",
                        "TiffinBox has become a lifesaver for me and my family. With hectic schedules and dietary restrictions, finding the time to prepare nutritious meals was a constant struggle. Thanks to TiffinBox, we now enjoy restaurant-quality meals without the hassle. The portion sizes are generous, and the flavors are always on point. Thank you for making healthy eating so effortless!",
                        "I can't say enough good things about TiffinBox! As a student balancing coursework and extracurricular activities, cooking meals often takes a backseat. TiffinBox has been a game-changer for me. The affordable pricing and customizable meal plans fit perfectly into my budget and dietary preferences. Plus, the food is so tasty, it's hard to believe it's also good for me!",
                        "TiffinBox has truly elevated my dining experience. Gone are the days of settling for mediocre takeout or spending hours in the kitchen. With TiffinBox, I get the best of both worlds – gourmet meals crafted with fresh, high-quality ingredients, delivered straight to my door. It's like having a personal chef without the hefty price tag. I'm hooked!",
                        "I've tried several meal delivery services in the past, but none compare to the excellence of TiffinBox. The attention to detail in each dish is evident, from the vibrant colors to the exquisite presentation. Not only does TiffinBox make eating healthy a breeze, but it also adds an element of luxury to my everyday routine. Thank you for exceeding my expectations time and time again!"]
    for txt in testimonial_text:
        tmp = Testimonial(user=TBUser.objects.get(id=choice(range(*user_ids))), comment=txt)
        tmp.save()
    return HttpResponse(content={"message": "OK"})
