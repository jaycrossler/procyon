from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from procyon.starsystemmaker.models import *
import locale


class PlanetModelAdmin(admin.ModelAdmin):
    model = PlanetModel
    exclude = ['parent_star', ]
    list_display = ['name', 'planet_type', 'mass', 'radius', 'surface_ocean_amount', 'other_name', 'parent_star', ]


class StarModelAdmin(admin.ModelAdmin):
    model = StarModel
    list_display = ['id', 'real_star_id', 'star', 'star_type', 'base_color', 'star_type_name', 'mass_in_sol', 'radius_in_sol', 'age_in_my']
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

    def real_star_id(self, obj):
        star = obj.star
        if star:
            return star.id
        else:
            return "Unknown"


class PlanetTypeAdmin(admin.ModelAdmin):
    model = PlanetType
    list_display = ['name', 'mass_range', 'radius_range', 'temperature_range', ]

admin.site.register(StarModel, StarModelAdmin)
admin.site.register(PlanetModel, PlanetModelAdmin)
admin.site.register(PlanetType, PlanetTypeAdmin)
