from django.shortcuts import render

from .models import Tiffin
from enum_maps import MEAL
from .forms import ExploreSearchForm, FilterForm


def explore(request):
    searchForm = ExploreSearchForm()
    filtersForm = FilterForm()
    query_set = (Tiffin.objects.all()
                 .values("tiffin_name", "image", "business_id__first_name", "business_id__last_name", "avg_rating",
                         "price"))
    tiffins = []
    if searchForm.is_valid() and 'query' in request.GET:
        search = request.GET.get("search")
        query_set = query_set.filter(tiffin_name__contains=search)
    else:
        query_set = query_set

    print(filtersForm.is_valid())
    print(filtersForm.changed_data)

    if filtersForm.is_valid() and filtersForm.changed_data:
        mealType = filtersForm.cleaned_data.get('meal_type')
        rating = filtersForm.cleaned_data.get('rating')
        calorie_min = filtersForm.cleaned_data.get('calorie_range')
        calorie_max = filtersForm.cleaned_data.get('calorie_range')
        price_min = filtersForm.cleaned_data.get('price_range')
        price_max = filtersForm.cleaned_data.get('price_range')
        print(mealType, rating)
        print(calorie_min, calorie_max, price_min, price_max)

        if mealType:
            query_set = query_set.filter(meal_type=mealType)

        if rating:
            query_set = query_set.filter(avg_rating__in=rating)
    else:
        query_set = query_set

    for tiffin in query_set:
        tiffins.append({"name": tiffin["tiffin_name"], "photo": tiffin["image"],
                        "business": tiffin["business_id__first_name"] + tiffin["business_id__last_name"],
                        "rating": list(range(int(round(tiffin["avg_rating"])))),
                        "price": tiffin["price"]})

    meal_types = Tiffin.objects.values_list("meal_type", flat=True).distinct()
    meal_types = [MEAL[i] for i in meal_types]
    return render(request, 'user_dashboard/explore.html', {'tiffins': tiffins,
                                                           "meal_types": meal_types})
