from faker import Faker
from django.db.utils import IntegrityError
from django.http import HttpResponse
from .models import TBUser, Schedule, Tiffin, Review, Testimonial

from random import choice

fake = Faker()


def insert_fake_data(request):
    businesses = [("foodex_tiffins", "FoodEX Budget Non-Veg Tiffins", "foodex@foodex.ca", "faker/business_1.jpeg"),
                  ("hashtag_co", "Hashtag Budget Veg Tiffins", "hashtag@hashtag.ca", "faker/business_2.jpeg"),
                  ("kaurs_kitchen", "Kaur's Kitchen Tiffins", "kar@kk.ca", "faker/business_3.jpeg"),
                  ("taco_king", "Taco King", "king@tk.ca", "faker/business_5.jpeg")]
    business_ids = (1, len(businesses) + 1)
    for ele in businesses:
        tmp = TBUser(username=ele[0], first_name=ele[1], email=ele[2], client_type=1,
                     profile_picture=ele[3], shipping_address=fake.address(), is_registered=True)
        tmp.set_password("admin@1234")
        try:
            tmp.save()
        except IntegrityError:
            pass

    user_ids = (business_ids[-1], business_ids[-1] + 8)
    for idx in range(*user_ids):
        profile = fake.simple_profile()
        tmp = TBUser(username=profile["username"], first_name=profile["name"], email=profile["mail"],
                     client_type=0,
                     profile_picture=f"faker/user_{idx - business_ids[-1] + 1}.jpeg",
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
