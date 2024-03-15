from math import ceil

from django import forms
from django.db.models import Max, Min

from user_dashboard.models import Tiffin


class ExploreSearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by business name or food item'}))


RATING_CHOICES = [
    ('5', '⭐⭐⭐⭐⭐'),
    ('4', '⭐⭐⭐⭐'),
    ('3', '⭐⭐⭐'),
    ('2', '⭐⭐'),
    ('1', '⭐'),
]


def create_price_range():
    min_ = float(Tiffin.objects.all().values_list('price', flat=True).annotate(Min('price')).order_by('price')[0])
    max_ = float(Tiffin.objects.all().values_list('price', flat=True).annotate(Max('price')).order_by('-price')[0])
    min_ = int(min_ - (min_ % 10))
    max_ = int(max_ - (max_ % 10)) + 10
    ranges = list(range(min_, max_, 10))
    ranges = list(zip(ranges, ranges[1:]))
    ranges = [(f"${r[0]} - ${r[1]}", f"${r[0]} - ${r[1]}") for r in ranges]
    return ranges


def create_calorie_range():
    min_ = float(Tiffin.objects.all().values_list('calories', flat=True)
                 .annotate(Min('calories')).order_by('calories')[0])
    max_ = float(Tiffin.objects.all().values_list('calories', flat=True)
                 .annotate(Max('calories')).order_by('-calories')[0])
    min_ = int(min_ - (min_ % 100))
    max_ = int(max_ - (max_ % 100)) + 100
    ranges = list(range(min_, max_, 100))
    ranges = list(zip(ranges, ranges[1:]))
    ranges = [(f"{r[0]} - {r[1]}", f"{r[0]} - {r[1]}") for r in ranges]
    return ranges


class FilterForm(forms.ModelForm):
    class Meta:
        model = Tiffin
        exclude = ["image", "tiffin_name", "tiffin_description", "schedule_id", "business_id"]
        widgets = {"meal_type": forms.CheckboxSelectMultiple(choices=Tiffin.MEAL),
                   "avg_rating": forms.CheckboxSelectMultiple(choices=RATING_CHOICES),
                   "price": forms.RadioSelect(choices=create_price_range()),
                   "calories": forms.RadioSelect(choices=create_calorie_range())}
        labels = {"avg_rating": "Rating"}
        required = []
