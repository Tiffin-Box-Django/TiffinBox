from django.shortcuts import render, get_object_or_404

from .models import Tiffin, Review
from enum_maps import MEAL


def explore(request):
    if request.method != 'GET':
        return {"error": "Method Not Allowed"}
    query_set = (Tiffin.objects.all()
                 .values("tiffin_name", "image", "business_id__first_name", "business_id__last_name", "avg_rating",
                         "price"))
    tiffins = []
    for tiffin in query_set:
        tiffins.append({"name": tiffin["tiffin_name"], "photo": tiffin["image"],
                        "business": tiffin["business_id__first_name"] + tiffin["business_id__last_name"],
                        "rating": list(range(int(round(tiffin["avg_rating"])))),
                        "price": tiffin["price"]})

    meal_types = Tiffin.objects.values_list("meal_type", flat=True).distinct()
    meal_types = [MEAL[i] for i in meal_types]
    return render(request, 'user_dashboard/explore.html', {'tiffins': tiffins,
                                                           "meal_types": meal_types})


def tiffindetails(request, tiffinid: int):
    tiffin = get_object_or_404(Tiffin, id=tiffinid)
    review_counts = Review.objects.filter(tiffin_id=tiffinid).count()
    reviews = Review.objects.all().values("user__first_name", "user__last_name", "comment", "rating", "created_date")
    reviews_grid, tmp = [], []
    for idx, review in enumerate(reviews):
        if idx % 3 != 0 or idx == 0:
            tmp.append(review)
        else:
            reviews_grid.append(tmp)
            tmp = [review]
    if tmp:
        reviews_grid.append(tmp)
    tiffin_extras = [("Delivery Frequency", tiffin.schedule_id.enum(), "calendar-week"),
                     ("Meal Plan", dict(tiffin.MEAL)[tiffin.meal_type], "basket"),
                     ("Calories", tiffin.calories, "lightning")]
    return render(request, 'user_dashboard/tiffindetails.html', {"tiffin": tiffin,
                                                                 "tiffin_extras": tiffin_extras,
                                                                 "review_counts": review_counts,
                                                                 "reviews_grid": reviews_grid})


def addcart(request, id):
    return None
