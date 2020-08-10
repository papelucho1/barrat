from django.contrib import admin

from application import models
# Register your models here.


admin.site.register(models.Answer)
admin.site.register(models.Test)
admin.site.register(models.Question)
admin.site.register(models.Profile)


