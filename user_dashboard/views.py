from django.shortcuts import render

from .models import Tiffin
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

def tiffindetails(request):
    # tiffin = Tiffin.objects.get(pk=1)
    return render(request, 'user_dashboard/tiffindetails.html')

def addcart(request, id):
    return None