from django import forms


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