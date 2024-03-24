from django.db.utils import Error

from django import forms
from django.db.models import Max, Min
from user_dashboard.models import Tiffin, TBUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password


class ExploreSearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search tiffins'}))


RATING_CHOICES = [
    ('5', '⭐⭐⭐⭐⭐'),
    ('4', '⭐⭐⭐⭐'),
    ('3', '⭐⭐⭐'),
    ('2', '⭐⭐'),
    ('1', '⭐'),
]


def create_price_range():
    try:
        if Tiffin.objects.all().count() == 0:
            return []
    except Error:
        return []
    min_ = float(Tiffin.objects.all().values_list('price', flat=True).annotate(Min('price')).order_by('price')[0])
    max_ = float(Tiffin.objects.all().values_list('price', flat=True).annotate(Max('price')).order_by('-price')[0])
    min_ = int(min_ - (min_ % 10))
    max_ = int(max_ - (max_ % 10)) + 10
    ranges = list(range(min_, max_, 10))
    ranges = list(zip(ranges, ranges[1:]))
    ranges = [(f"${r[0]} - ${r[1]}", f"${r[0]} - ${r[1]}") for r in ranges]
    return ranges


def create_calorie_range():
    try:
        if Tiffin.objects.all().count() == 0:
            return []
    except Error:
        return []
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
        widgets = {"meal_type": forms.Select(choices=Tiffin.MEAL),
                   "avg_rating": forms.CheckboxSelectMultiple(choices=RATING_CHOICES),
                   "price": forms.RadioSelect(choices=create_price_range()),
                   "calories": forms.RadioSelect(choices=create_calorie_range())}
        labels = {"avg_rating": "Rating"}


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    def clean_email(self):
        email = self.cleaned_data['email']
        if TBUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if TBUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name.capitalize()

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        validate_password(password1)
        return password1

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        elif len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be 10 digits long.")
        return phone_number

    class Meta:
        model = TBUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = TBUser
        fields = ['profile_picture', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'shipping_address']
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not username:
            self.add_error('username', 'Username cannot be empty')
        user = TBUser.objects.filter(username=username)

        if user.count() > 1:
            raise forms.ValidationError('Username is already in use.')

        if not email:
            self.add_error('email', 'Email address cannot be empty')

        return cleaned_data