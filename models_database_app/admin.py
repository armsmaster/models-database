from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Owner)
admin.site.register(models.Model)
admin.site.register(models.Version)
admin.site.register(models.Attribute)
admin.site.register(models.ModelAttribute)
admin.site.register(models.VersionAttribute)
admin.site.register(models.ModelAttributeRecord)
admin.site.register(models.VersionAttributeRecord)