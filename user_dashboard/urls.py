from django.urls import path
from . import views

app_name = 'user_dashboard'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('explore/', views.explore, name='explore'),
    path('tiffin/<int:tiffinid>', views.tiffindetails, name='tiffindetails'),
    path('addcart/<id>', views.addcart, name='add_to_cart')
]
