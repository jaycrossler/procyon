from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from procyon.starsystemmaker.models import *
import locale
from django.http import HttpResponseRedirect

class PlanetModelAdmin(admin.ModelAdmin):
    model = PlanetModel
    exclude = ['parent_star', ]
    list_display = ['name', 'planet_type', 'mass', 'radius', 'surface_ocean_amount', 'other_name', 'parent_star', ]


def make_initialized(modeladmin, request, queryset):
    for obj in queryset:
        obj.build_model(forced=True)
make_initialized.short_description = "Initialize all variables of selected stars"


def make_randomized(modeladmin, request, queryset):
    for obj in queryset:
        obj.build_model(forced=False)
make_randomized.short_description = "Randomize variables of selected stars based on random seed"


def view_star_as_json(modeladmin, request, queryset):
    star = queryset[0].star
    if star and star.id:
        star_id = star.id
        return HttpResponseRedirect("/maker/star/{0}".format(star_id))
view_star_as_json.short_description = "View star JSON info"


class StarModelAdmin(admin.ModelAdmin):
    model = StarModel
    list_display = ['id', 'real_star_id', 'star', 'star_type', 'base_color', 'star_type_name', 'mass_in_sol', 'radius_in_sol', 'age_in_my']
    exclude = ['star', ]
    search_fields = ['star', ]
    list_filter = ['star_type', ]
    actions = [make_initialized, make_randomized, view_star_as_json]

    def star_type_name(self, obj):
        star_type = obj.star_type
        if star_type:
            output = obj.star_type.name.capitalize()
        else:
            output = "Unknown"
        return output

    def mass_in_sol(self, obj):
        output = obj.guessed_mass
        if output:
            output = "{0:.2f}".format(output)
        else:
            output = "Not Yet Initialized"
        return output

    def radius_in_sol(self, obj):
        output = obj.guessed_radius
        if output:
            output = "{0:.2f}".format(output)
        else:
            output = "Not Yet Initialized"
        return output

    def age_in_my(self, obj):
        output = obj.guessed_mass
        if output:
            output = locale.format("%d", obj.guessed_age, grouping=True)
        else:
            output = "Not Yet Initialized"
        return output

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
