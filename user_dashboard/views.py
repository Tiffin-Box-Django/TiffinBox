from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Tiffin, Review
from enum_maps import MEAL
from .forms import ExploreSearchForm, FilterForm


def explore(request):
    searchForm = ExploreSearchForm()
    filtersForm = FilterForm()
    query_set = Tiffin.objects.all().values("tiffin_name", "image", "business_id__first_name",
                                            "business_id__last_name", "avg_rating", "price", "id")
    tiffins = []
    if 'query' in request.GET:
        search = request.GET.get("search")
        query_set = query_set.filter(tiffin_name__contains=search)

    if filtersForm.changed_data and False:
        mealType = filtersForm.cleaned_data.get('meal_type')
        rating = filtersForm.cleaned_data.get('rating')
        # calorie_min = filtersForm.cleaned_data.get('calorie_range')
        # calorie_max = filtersForm.cleaned_data.get('calorie_range')
        # price_min = filtersForm.cleaned_data.get('price_range')
        # price_max = filtersForm.cleaned_data.get('price_range')

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
                        "price": tiffin["price"], "id": tiffin["id"]})

    paginator = Paginator(tiffins, 9)  # Show 9 dishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_dashboard/explore.html',
                  {'searchForm': searchForm, 'filtersForm': filtersForm,
                   'tiffins': page_obj, "filter_params": {}})


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
