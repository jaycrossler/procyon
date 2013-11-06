from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from starcatalog.models import *


class StarAdmin(admin.ModelAdmin):
    model = Star
    list_display = ['name']

admin.site.register(Star, StarAdmin)
