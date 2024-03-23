from django.urls import path
from . import views, faker_view

app_name = 'user_dashboard'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('fake-data/', faker_view.insert_fake_data, name='fake-data'),
    path('explore/', views.explore, name='explore'),
    path('tiffin/<int:pk>/', views.TiffinDetails.as_view(), name='tiffindetails'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', views.UserLogin.as_view(), name='acc-login'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('deleteCartItem/<int:id>/', views.deleteCartItem, name='deleteCartItem'),
    path('placeOrder/', views.placeOrder, name='placeOrder'),
    path('OrderHistory/', views.order_history, name='OrderHistory'),
    path('update-cart/', views.update_cart, name='update-cart'),
    path('add-review/<int:tiffinid>', views.add_review, name='add-review'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='editprofile'),
    path('businessdetails/<int:pk>/', views.business_details, name='businessdetails')
]
