from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
#import json
from django.utils import simplejson
from django.core import serializers

class Star(models.Model):
    """
    It's full of stars
    """
    name = models.CharField(help_text="Star name", max_length=200, unique=True)

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Stars in the Galaxy'
#        ordering = ['distance_to_sol']
