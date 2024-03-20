from bootstrap_colors.views import BootstrapColorsView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("user_dashboard.urls")),
    path('business/', include("business_dashboard.urls")),
    # this is for overriding the bootstrap color variables
    path('colors.css', BootstrapColorsView.as_view(), name='colors'),
    path('reset_password',
         auth_views.PasswordResetView.as_view(template_name='commons/forgot-password.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='commons/reset-password-sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='commons/reset-password.html'),
         name='password_reset_confirm'),
    path('reset_password_omplete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='commons/reset-password-complete.html'),
         name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
