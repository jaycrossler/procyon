from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from starcatalog.models import *


class StarAdmin(admin.ModelAdmin):
    model = Star
    list_display = ['id', 'gliese', 'HIP', 'HD', 'proper_name', 'distance_parsecs', ]
    list_filter = ['proper_name', 'distance_parsecs']

class PlanetAdmin(admin.ModelAdmin):
    model = Planet
    list_display = ['name', 'mass', 'gliese', 'HIP', 'HD', ]
    list_filter = ['name', ]


admin.site.register(Star, StarAdmin)
admin.site.register(Planet, PlanetAdmin)
