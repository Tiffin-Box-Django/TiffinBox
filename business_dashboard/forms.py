from django import forms
from user_dashboard.models import Tiffin, TBUser


class TiffinForm(forms.ModelForm):
    class Meta:
        model = Tiffin
        fields = ['tiffin_name', 'tiffin_description', 'image', 'meal_type', 'calories', 'price',
                  'free_delivery_eligible']
        labels = {'tiffin_name': 'Tiffin Name',
                  'tiffin_description': 'Tiffin Description',
                  'image': 'Image',
                  'meal_type': 'Meal Type',
                  'calories': 'Calories',
                  'price': 'Price',
                  'free_delivery_eligible': 'Free Delivery'
                  }


class SignUpForm(forms.ModelForm):
    class Meta:
        model = TBUser
        fields = ['username', 'email', 'password', 'phone_number', 'is_registered', 'shipping_address']
        labels = {'username': 'Username', 'email': 'Email', 'password': 'Password', 'phone_number': 'Phone Number',
                  'is_registered': 'Is your Business registered?', 'shipping_address': 'Business Address'},
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'osmows...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'hello@osmows.ca...'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control', 'placeholder': '5196767230'}),
            'is_registered': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '3'})
        }
