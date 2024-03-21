from django.urls import path
from . import views, faker_view

app_name = 'user_dashboard'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('fake-data/', faker_view.insert_fake_data, name='fake-data'),
    path('explore/', views.explore, name='explore'),
    path('tiffin/<int:pk>/', views.TiffinDetails.as_view(), name='tiffindetails'),
    path('addcart/<id>', views.addcart, name='add_to_cart'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('update-cart/', views.update_cart, name='update-cart'),
    path('add-review/<int:tiffinid>', views.add_review, name='add-review'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]
