from django.urls import path
from . import views

app_name = 'user_dashboard'
urlpatterns = [
    path('explore/', views.explore, name='explore'),
    path('tiffindetails/<int:tiffin_id>/', views.tiffindetails, name='tiffindetails')
]
