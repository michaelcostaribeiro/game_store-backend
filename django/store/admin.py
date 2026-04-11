from django.contrib import admin
from . import models

admin.site.register(models.Game)
admin.site.register(models.Genre)
admin.site.register(models.Platform)
admin.site.register(models.Console)