from django.contrib.contenttypes import generic
from django.contrib.gis import admin
from models import *


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['user', 'text', 'importance', 'reviewed']
    extra = 1
    verbose_name = "Story Comments"


class StoryImageInline(admin.TabularInline):
    model = StoryImage
    extra = 2


class StoryAdmin(admin.ModelAdmin):
    model = Story
    list_display = ['name', 'id', 'active', 'anthology', 'tags', 'type', 'year_min', 'year_max', ]
    fields = [('active', 'anthology', 'tags', 'type'), 'name', 'description',
              ('year_min', 'year_max', 'times_used', 'force_usage'), ('requirements', 'story',), ('choices', 'variables',),
              ('following_stories', 'not_if_previous_stories',), ]
    search_fields = ['id', 'name', 'anthology', 'tags', 'type', 'description']
    list_filter = ('anthology', 'type',)

    # actions = ['refresh']
    inlines = [CommentInline, StoryImageInline]
    save_as = True
    view_on_site = True


admin.site.register(Story, StoryAdmin)
admin.site.register(Comment)
