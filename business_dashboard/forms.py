from django import forms
from user_dashboard.models import Tiffin

class TiffinForm(forms.ModelForm):
    class Meta:
        model = Tiffin
        fields = ['tiffin_name', 'tiffin_description', 'image', 'meal_type', 'calories', 'price', 'free_delivery_eligible']
        labels= {'tiffin_name': 'Tiffin Name',
                 'tiffin_description': 'Tiffin Description',
                 'image': 'Image',
                 'meal_type': 'Meal Type',
                 'calories': 'Calories',
                 'price': 'Price',
                 'free_delivery_eligible': 'Free Delivery'
                 }
