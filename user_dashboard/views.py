from django.shortcuts import render
from django.db.models import F

from .models import Tiffin


def explore(request):
    if request.method != 'GET':
        return {"error": "Method Not Allowed"}
    query_set = (Tiffin.objects.all()
                 .values("tiffin_name", "image", "business_id__first_name", "business_id__last_name", "avg_rating")
                 .annotate(name=F("tiffin_name"), photo=F("image"), business=F("business_id__first_name"),
                           rating=F("avg_rating")))
    tiffins = []
    for tiffin in query_set:
        tiffins.append({"name": tiffin["tiffin_name"], "photo": tiffin["image"],
                        "business": tiffin["business_id__first_name"] + tiffin["business_id__last_name"],
                        "rating": list(range(int(round(tiffin["avg_rating"]))))})
    return render(request, 'user_dashboard/explore.html', {'tiffins': tiffins})
