from django import forms
from user_dashboard.models import Tiffin, TBUser, Schedule
from django.contrib.auth.forms import UserCreationForm


class AddTiffinForm(forms.ModelForm):
    class Meta:
        model = Tiffin
        exclude = ['business_id', 'avg_rating'] #business_id will be fetched from current user who is logged in

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='You must enter a valid email address')

    def validate_username(self):
        username = self.cleaned_data['username']
        if TBUser.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Username '{username}' is already in use")
        return username

    def validate_email(self):
        email = self.cleaned_data['email']
        if TBUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email '{email}' is already in use")
        return email

    class Meta:
        model = TBUser
        fields = ['first_name', 'last_name', 'is_registered', 'phone_number', 'shipping_address', 'username', 'email', 'password1', 'password2', 'profile_picture']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'is_registered': 'Is your business registered?',
                  'phone_number': 'Phone Number', 'shipping_address': 'Business Address', 'username': 'Username',
                  'email': 'Email', 'password1': 'Password', 'password2': 'Confirm Password'}


class EditTiffinForm(forms.ModelForm):
    class Meta:
        model = Tiffin
        fields = ['tiffin_name', 'tiffin_description', 'meal_type', 'calories', 'price', 'free_delivery_eligible', 'image']
        labels = {'tiffin_name': 'Name', 'tiffin_description': 'Description', 'meal_type': 'Meal Type',
                  'free_delivery_eligible': 'Do you provide free delivery for this tiffin?', 'schedule_id': 'Schedule'}

    # for populating with foreign key data
    def __init__(self, *args, **kwargs):
        super(EditTiffinForm, self).__init__(*args, **kwargs)
        self.fields['schedule_id'] = forms.ModelChoiceField(queryset=Schedule.objects.all(), label='Schedule')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = TBUser
        fields = ['profile_picture', 'username','first_name', 'last_name', 'email', 'phone_number', 'shipping_address']
