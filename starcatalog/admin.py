from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from starcatalog.models import *


class StarAdmin(admin.ModelAdmin):
    model = Star
    list_display = ['id', 'gliese', 'HIP', 'HD', 'proper_name', 'distance_parsecs', ]
    list_filter = ['gliese', 'HIP', 'HD', 'proper_name', 'distance_parsecs']

class PlanetAdmin(admin.ModelAdmin):
    model = Planet
    list_display = ['name', 'mass', 'gliese', 'HIPP', 'HD', ]
    list_filter = ['name', 'gliese', 'HIPP', 'HD', ]


admin.site.register(Star, StarAdmin)
admin.site.register(Planet, PlanetAdmin)
