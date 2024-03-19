from django.urls import path
from . import views

app_name = 'business_dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('tiffin/', views.tiffin, name='tiffin'),
    path('tiffin/add', views.add_tiffin, name='add_tiffin'),
    path('profile/<str:username>', views.business_profile, name='profile'),
    path('sign-up/', views.signup, name='sign-up'),
    path('login', views.businessLoginPage, name='login'),
    path('tiffin/edit/<int:tiffin_id>/', views.edit_tiffin, name="edit_tiffin"),
    path('logout/', views.logout_view, name="logout"),
    path('orders/<int:order_status>', views.orders, name="orders"),
    path('orders/status/update/<int:order_id>', views.update_order_status, name="update_order_status")
]
