from django.contrib import admin
from ShoppingApp import  models
# Register your models here.
# Register your models here.


# admin.site.register(models.AppSettings)

admin.site.register(models.BillRecordMain)
admin.site.register(models.BillRecordSub)
admin.site.register(models.GoodsRecord)
admin.site.register(models.ShoppingCar)
