# -*- coding: utf-8 -*-

import json
import os
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from procyon.generators.story_helpers import check_requirements
import uuid


class SnippetBase(models.Model):
    """
    An object builder based on constraints
    """

    active = models.BooleanField(default=True, help_text='If checked, this object will be listed in the active list',
                                 db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    anthology = models.CharField(max_length=200, blank=True, default="",
                                 help_text='Grouping of objects - could be the world or location. Only items matching this will be returned')
    name = models.CharField(max_length=200, default="Text", blank=True,
                            help_text='Name of the object for display and search')
    tags = models.CharField(max_length=200, default="", null=True, blank=True, help_text='Tags to describe this object')

    requirements = models.TextField(
        help_text="List of all requirements that must be met before this object is an option, eg: year>1400",
        blank=True, null=True)

    def filter_by_requirements(self, world_data):
        return check_requirements(self.requirements, world_data)

    def __unicode__(self):
        anthology = ""
        if self.anthology:
            anthology = '[%s] ' % (self.anthology, )
        return '%s%s' % (anthology, self.name)


class Story(SnippetBase):
    """
    A story object based on constraints
    """

    type = models.CharField(db_index=True, max_length=200, default="Quest",
                            help_text='Type of story (e.g. Quest, Tale, Location, Conversation)')

    uuid = models.CharField(db_index=True, max_length=100, default=uuid.uuid4, null=True, blank=True)

    year_min = models.IntegerField(db_index=True, default=1000,
                                   help_text="Minimum Earth Year Number that this story can occur in (e.g. 1776)")
    year_max = models.IntegerField(db_index=True, default=2100,
                                   help_text="Maximum Earth Year Number that this story can occur in (e.g. 1801)")

    times_used = models.IntegerField(default=0,
                                     help_text="How often this story has been reported to be used")

    story = JSONField(help_text="Story with images, details, choices, sub-stories, and effects")
    variables = JSONField(help_text="Objects, People, Names within the story that can be overridden")
    # TODO: Allow variables to be referenced by other stories

    metadata = JSONField(default={"max_times_usable": 1, "force_usage": 0},
                         help_text="Additional details, ex: Pointers to stories that can occur afterwards (with likelihood)")

    @property
    def comments(self):
        return Comment.objects.filter(story=self).order_by('-importance, created_at')

    @property
    def open_comments(self):
        return Comment.objects.filter(story=self).having(reviewed=False).order_by('-importance, created_at')

    def to_json(self):
        return json.dumps({
                              "id": str(self.id),
                              "uuid": str(self.uuid),

                              "name": self.name,
                              "active": self.active,
                              "anthology": self.anthology,
                              "tags": self.tags,
                              "type": self.type,
                              "year_min": str(self.year_min),
                              "year_max": str(self.year_max),

                              "requirements": self.requirements,
                              "story": self.story,
                              "variables": self.variables,
                              "metadata": self.metadata,

                              "images": [
                                  {"url": str(i.image), "width": int(i.image.width), "height": int(i.image.height)} for
                                  i in self.images.all()]
                          }, ensure_ascii=True)

    def get_absolute_url(self):
        return reverse('story-detail', args=[self.id])

    def __unicode__(self):
        anthology = ""
        if self.anthology:
            anthology = '[%s] ' % (self.anthology, )
        name_str = '%s%s : (%s - %s)' % (anthology, self.name, self.year_min, self.year_max)
        return name_str

    class Meta:
        abstract = False
        ordering = ('year_min', '-created_at',)
        verbose_name_plural = "stories"


class Comment(models.Model):
    """
    Track comments of a story
    """
    user = models.ForeignKey(User, blank=True, null=True, help_text="User who made comment")
    story = models.ForeignKey(Story, blank=False, null=False, help_text="Associated story for comment")
    text = models.TextField(blank=True, default="", max_length=400)
    rating = models.IntegerField(default=3, help_text="How much do you like/enjoy this story? 1 for low, 5 for high")

    created_at = models.DateTimeField(auto_now_add=True)

    importance = models.IntegerField(default=0,
                                     help_text="How critical is it to look at this comment?  0 for low, 5 for high")
    reviewed = models.BooleanField(default=False,
                                   help_text="Has this comment been reviewed? Checked means to not show as an open comment")

    def __unicode__(self):
        comment_obj = '%s Comment on %s' % (self.user, self.story)
        return comment_obj

    def to_dict(self):
        format = "%D %H:%M:%S"
        o = {'user': self.user.username, 'timestamp': self.created_at.strftime(format), 'text': self.text}
        return o

    class Meta:
        abstract = False
        ordering = ('-importance', '-created_at',)


def get_storyimage_path(instance, filename):
    return os.path.join('story_images/', str(instance.story.id), filename)


class StoryImage(models.Model):
    story = models.ForeignKey(Story, related_name="images")
    image = models.ImageField(upload_to=get_storyimage_path, blank=True, null=True,
                              help_text="Upload an icon (now only in Admin menu) that will go with the story here, then refer to the image by name (without path) in your story")


class Component(SnippetBase):
    effects = JSONField(null=True, blank=True, help_text="Effects upon user when applied", default="[]")
    properties = JSONField(null=True, blank=True, help_text="Metadata to use when this component is applied",
                           default="{}")
    weighting = models.IntegerField(default=10,
                                    help_text="How likely is it that this should be picked? 1 = very unlikey, 10 = normal, 100 = likely")

    type = models.CharField(db_index=True, max_length=200, default="Power", blank=True,
                            help_text='Type of item verbal grouping (e.g. Power, Adjective, Quirk, First Name, etc)')

    def to_json(self):
        return json.dumps({
                              "id": str(self.id),
                              "name": self.name,
                              "active": self.active,
                              "anthology": self.anthology,
                              "tags": self.tags,
                              "type": self.type,
                              "weighting": self.weighting,

                              "requirements": self.requirements,
                              "properties": self.properties,
                              "effects": self.effects
                          }, ensure_ascii=True)

    class Meta:
        ordering = ('type', 'name',)
