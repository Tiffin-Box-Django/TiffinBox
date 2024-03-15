from bootstrap_colors.views import BootstrapColorsView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user_dashboard.urls")),
    path('business/', include("business_dashboard.urls")),
    # this is for overriding the bootstrap color variables
    path('colors.css', BootstrapColorsView.as_view(), name='colors')
]
