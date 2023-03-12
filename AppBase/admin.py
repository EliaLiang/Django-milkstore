from django.contrib import admin
from AppBase import  models
# Register your models here.
# Register your models here.
admin.site.register(models.UserDict)

admin.site.register(models.AppSettings)


admin.site.register(models.AppMenuDict)


admin.site.register(models.EmailSendFromDefaultSettings)

admin.site.register(models.AppDefaultIocn)