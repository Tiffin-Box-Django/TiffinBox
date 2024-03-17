from django import forms
<<<<<<< HEAD


class ExploreSearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by business name or food item'}))


RATING_CHOICES = [
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
]

MEAL_TYPE = [
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner')
]


class FilterForm(forms.Form, forms.RegexField):
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    meal_type = forms.ChoiceField(choices=MEAL_TYPE, widget=forms.CheckboxSelectMultiple, required=False)
    calorie_range = forms.IntegerField(label='Calorie Range', required=False)
    price_range = forms.IntegerField(label='Price Range', required=False)

    widgets = {
        'calorie_range': forms.RangeInput(attrs={'type': 'range', 'min': 0, 'max': 1000}),
        'price_range': forms.RangeInput(attrs={'type': 'range', 'min': 0, 'max': 1000}),
    }
=======
from django.db.models import Max, Min

from user_dashboard.models import Tiffin


class ExploreSearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'w-75',
                                                                     'placeholder': 'Search tiffins or businesses'}))


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
>>>>>>> 90e0fb0a7ffdf76bad4852e6326f4f7f73948c91
