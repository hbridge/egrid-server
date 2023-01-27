from django.contrib.gis import admin
from .models import EGridPlant

admin.site.register(EGridPlant, admin.ModelAdmin)