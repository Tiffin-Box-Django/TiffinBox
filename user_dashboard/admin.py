from django.contrib import admin

from . import models
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "expire_date", 'user_id', 'username']

    class Meta:
        model = Session

    def user_id(self, obj):
        return obj.get_decoded().get('_auth_user_id')
    def username(self, obj):
        return obj.get_decoded().get('username')


class TBUserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "username", "email", 'client_type']



# Register your models here.
admin.site.register(models.TiffinItemList)
admin.site.register(models.Schedule)
admin.site.register(models.TBUser, TBUserAdmin)
admin.site.register(models.Tiffin)
admin.site.register(models.TiffinContent)
admin.site.register(models.Testimonial)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Review)
admin.site.register(Session, SessionAdmin)
