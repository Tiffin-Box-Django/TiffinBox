from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user_dashboard.urls")),
    path('business/', include("admin_dashboard.urls"))
]
