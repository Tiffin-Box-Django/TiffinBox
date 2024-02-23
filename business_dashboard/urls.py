from django.urls import path
from . import views

app_name = 'business_dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('tiffin/', views.tiffin, name='tiffin')
]
