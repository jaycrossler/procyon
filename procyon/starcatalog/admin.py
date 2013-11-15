from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from procyon.starcatalog.models import *
import locale



class StarAdmin(admin.ModelAdmin):
    model = Star
    list_display = ['id', 'proper_name', 'gliese', 'HIP', 'HD', 'distance_ly', 'known_planet_count', 'possibly_habitable', 'spectrum', 'web_color', ]
    search_fields = ['gliese', 'HIP', 'HD', 'proper_name', ]


class PlanetAdmin(admin.ModelAdmin):
    model = Planet
    list_display = ['name', 'mass', 'gliese', 'HIP', 'HD', ]
    search_fields = ['name', 'gliese', 'HIP', 'HD', ]


class StarTypeAdmin(admin.ModelAdmin):
    model = StarType
    list_display = ['symbol', 'name', 'base_color', 'mass_range', ]


class StarModelAdmin(admin.ModelAdmin):
    model = StarModel
    list_display = ['star', 'star_type', 'base_color', 'star_type_name', 'mass_in_sol', 'radius_in_sol', 'age_in_my', ]
    exclude = ['star', ]
    search_fields = ['star', ]
    list_filter = ['star_type', ]

    def star_type_name(self, obj):
        star_type = obj.star_type
        if star_type:
            output = obj.star_type.name.capitalize()
        else:
            output = "Unknown"
        return output

    def mass_in_sol(self, obj):
        return "{0:.2f}".format(obj.guessed_mass)

    def radius_in_sol(self, obj):
        return "{0:.2f}".format(obj.guessed_radius)


    def age_in_my(self, obj):
        locale.setlocale(locale.LC_ALL, 'en_US')
        return locale.format("%d", obj.guessed_age, grouping=True)


class PlanetTypeAdmin(admin.ModelAdmin):
    model = Planet
    list_display = ['name', 'mass_range', 'radius_range', 'temperature_range', ]


admin.site.register(Star, StarAdmin)
admin.site.register(StarModel, StarModelAdmin)
admin.site.register(StarType, StarTypeAdmin)
admin.site.register(Planet, PlanetAdmin)
admin.site.register(PlanetType, PlanetTypeAdmin)
