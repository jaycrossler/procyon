from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['user', 'text', 'importance', 'reviewed']
    extra = 1
    verbose_name = "Story Comments"


class StoryImageInline(admin.TabularInline):
    model = StoryImage
    extra = 2


class StoryResource(resources.ModelResource):

    class Meta:
        model = Story


class StoryAdmin(ImportExportModelAdmin):
    model = Story
    list_display = ['name', 'id', 'active', 'anthology', 'tags', 'type', 'year_min', 'year_max']
    fields = [('active', 'anthology', 'tags', 'type'), 'name',
              ('year_min', 'year_max', 'times_used'), ('variables', 'story',), 'requirements', 'uuid']
    search_fields = ['id', 'name', 'anthology', 'tags', 'type']
    list_filter = ('anthology', 'type',)
    resource_class = StoryResource

    # actions = ['refresh']
    inlines = [CommentInline, StoryImageInline]
    save_as = True
    view_on_site = True


class ComponentResource(resources.ModelResource):

    class Meta:
        model = Component


class ComponentAdmin(ImportExportModelAdmin):
    model = Component
    save_as = True
    list_display = ['name', 'anthology', 'type', 'tags']
    search_fields = ['name', 'anthology', 'type']
    list_filter = ('anthology', 'type',)
    resource_class = ComponentResource
    pass


admin.site.register(Story, StoryAdmin)
admin.site.register(Comment)
admin.site.register(Component, ComponentAdmin)
