from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from procyon.starcatalog.models import *


class StarAdmin(admin.ModelAdmin):
    model = Star
    list_display = ['id', 'proper_name', 'gliese', 'HIP', 'HD', 'distance_ly', 'known_planet_count', 'possibly_habitable', 'spectrum', ]
    search_fields = ['gliese', 'HIP', 'HD', 'proper_name', ]


class PlanetAdmin(admin.ModelAdmin):
    model = Planet
    list_display = ['name', 'mass', 'gliese', 'HIP', 'HD', ]
    search_fields = ['name', 'gliese', 'HIP', 'HD', ]


class StarTypeAdmin(admin.ModelAdmin):
    model = StarType
    list_display = ['symbol', 'name', 'base_color', 'mass_range', ]


class StarLuminosityTypeAdmin(admin.ModelAdmin):
    model = StarLuminosityType
    list_display = ['symbol', 'short_name', ]


admin.site.register(Star, StarAdmin)
admin.site.register(Planet, PlanetAdmin)
admin.site.register(StarType, StarTypeAdmin)
admin.site.register(StarLuminosityType, StarLuminosityTypeAdmin)
