from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.TiffinItemList)
admin.site.register(models.Schedule)
admin.site.register(models.TBUser)
admin.site.register(models.Tiffin)
admin.site.register(models.TiffinContents)
admin.site.register(models.Testimonial)
admin.site.register(models.Orders)
admin.site.register(models.OrderItem)
admin.site.register(models.Review)