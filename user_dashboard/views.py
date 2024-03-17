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
    return render(request, 'user_dashboard/tiffindetails.html', {"tiffin": tiffin,
                                                                 "review_counts": review_counts})


def addcart(request, id):
    return None
