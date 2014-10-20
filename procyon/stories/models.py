# -*- coding: utf-8 -*-

import json
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User


class Story(models.Model):
    """
    A story object based on constraints
    """

    active = models.BooleanField(default=True, help_text='If checked, this story will be listed in the active list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    anthology = models.CharField(max_length=200, blank=True, default="",
                                 help_text='Grouping of stories - could be the world or location. Only stories matching this will be returned')
    name = models.CharField(max_length=200, default="Story", help_text='Name of the story for display and search')
    description = models.TextField(blank=True, default="",
                                   help_text='Details of this story not to be displayed in the story itself')
    tags = models.CharField(max_length=200, default="", null=True, help_text='Tags to describe this story')
    type = models.CharField(max_length=200, default="Quest",
                            help_text='Type of story (e.g. Quest, Tale, Location, Conversation)')

    year_min = models.IntegerField(default=1000,
                                   help_text="Minimum Year Number that this story can occur in (e.g. 1776)")
    year_max = models.IntegerField(default=2100,
                                   help_text="Maximum Year Number that this story can occur in (e.g. 1801)")

    times_used = models.IntegerField(default=0,
                                     help_text="Pointers to stories that can occur afterwards (with likelihood)")
    force_usage = models.IntegerField(default=0,
                                      help_text="For testing, how many times should this story be shown immediately if someone passes in that developer=true?")

    requirements = JSONField(help_text="List of all requirements that must be met before this story is an option")
    story = JSONField(help_text="Story and details")
    options = JSONField(help_text="Options user can take after story")

    following_stories = JSONField(help_text="Pointers to stories that can occur afterwards (with likelihood)")
    not_if_previous_stories = JSONField(
        help_text="Pointers to stories that prevent this story from being a possible response")

    @property
    def comment_log(self):
        return Comment.objects.filter(story=self).order_by('-importance, created_at')

    def __unicode__(self):
        anthology = ""
        if self.anthology:
            anthology = '[%s] ' % (self.anthology, )
        name_str = '%s%s : (%s - %s)' % (anthology, self.name, self.year_min, self.year_max)
        return name_str

    class Meta:
        abstract = False
        ordering = ('-created_at',)
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
                                   help_text="Has this comment been reviewed? Checked means not to show as an open comment")

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
