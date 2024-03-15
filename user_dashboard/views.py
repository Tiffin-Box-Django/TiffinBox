from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Tiffin
from enum_maps import MEAL
from .forms import ExploreSearchForm, FilterForm


def explore(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        if post_data["avg_rating"]:
            post_data["avg_rating"] = float(post_data["avg_rating"])
        filters_form = FilterForm(post_data)
        if filters_form.is_valid():
            tiffins = Tiffin.objects.filter(
                **{k: v for k, v in filters_form.cleaned_data.items() if v != '' and v is not None})
        else:
            tiffins = []
    else:
        filters_form = FilterForm()
        tiffins = Tiffin.objects.all().values("tiffin_name", "image", "business_id__first_name",
                                              "business_id__last_name", "avg_rating", "price", "id")

    formatted_tiffins = []
    for tiffin in tiffins:
        formatted_tiffins.append({"name": tiffin.tiffin_name, "photo": tiffin.image,
                                  "business": tiffin.business_id.first_name + tiffin.business_id.last_name,
                                  "rating": list(range(int(round(tiffin.avg_rating)))),
                                  "price": tiffin.price, "id": tiffin.id})
    search_form = ExploreSearchForm()
    return render(request, 'user_dashboard/explore.html',
                  {'searchForm': search_form, 'filtersForm': filters_form,
                   'tiffins': formatted_tiffins, "filter_params": {}})


def tiffindetails(request, tiffin_id):
    return Tiffin.objects.get(id=tiffin_id)
