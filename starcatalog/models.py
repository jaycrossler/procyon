from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
#import json
from django.utils import simplejson
from django.core import serializers


class Star(models.Model):
    """
    It's full of stars.
    Current version imported from the HYG Stellar database http://www.astronexus.com/node/34
    CSV maintained at https://github.com/astronexus/HYG-Database/blob/master/hygfull.csv
    """
#    star_id = models.PositiveIntegerField(help_text="ID from hygxyz.csv", blank=True, null=True)
    HIP = models.PositiveIntegerField(help_text="Hipparcos Catalog number", blank=True, null=True)
    HD = models.PositiveIntegerField(help_text="The star's ID in the Henry Draper catalog, if known.", blank=True, null=True)
    HR = models.PositiveIntegerField(help_text="The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.", blank=True, null=True)
    gliese = models.CharField(max_length=40, help_text="The star's ID in the third edition of the Gliese Catalog of Nearby Stars.", blank=True, null=True)
    bayer_flamsteed = models.CharField(max_length=40, help_text="The Bayer / Flamsteed designation, from the Fifth Edition of the Yale Bright Star Catalog. This is a combination of the two designations. The Flamsteed number, if present, is given first; then a three-letter abbreviation for the Bayer Greek letter; the Bayer superscript number, if present; and finally, the three-letter constellation abbreviation. Thus Alpha Andromedae has the field value '21Alp And', and Kappa1 Sculptoris (no Flamsteed number) has 'Kap1Scl'.", blank=True, null=True)
    proper_name = models.CharField(max_length=100, help_text="A common name for the star", blank=True, null=True)
    RA = models.FloatField(help_text="The star's right ascension for epoch 2000.0", blank=True, null=True)
    dec = models.FloatField(help_text="The star's right declination for epoch 2000.0", blank=True, null=True)
    distance_parsecs = models.FloatField(help_text="Distance in Parsecs, (Light Years * 4.)", blank=True, null=True)
    PMRA = models.FloatField(help_text="", blank=True, null=True)
    PMDec = models.FloatField(help_text="", blank=True, null=True)
    RV = models.FloatField(help_text="", blank=True, null=True)
    mag = models.FloatField(help_text="Brightness from Earth", blank=True, null=True)
    abs_mag = models.FloatField(help_text="Brightness from 10 parsecs", blank=True, null=True)
    spectrum = models.CharField(max_length=40, help_text="Color Spectrum", blank=True, null=True)
    color_index = models.FloatField(help_text="", blank=True, null=True)
    X = models.FloatField(help_text="Galactic X Coordinate", blank=True, null=True)
    Y = models.FloatField(help_text="Galactic Y Coordinate", blank=True, null=True)
    Z = models.FloatField(help_text="Galactic Z Coordinate", blank=True, null=True)
    VX = models.FloatField(help_text="Annual change in Galactic X Coordinate", blank=True, null=True)
    VY = models.FloatField(help_text="Annual change in Galactic Y Coordinate", blank=True, null=True)
    VZ = models.FloatField(help_text="Annual change in Galactic Z Coordinate", blank=True, null=True)

    def __unicode__(self):
        name = self.proper_name
        if not name:
            if self.bayer_flamsteed:
                name = self.bayer_flamsteed
            elif self.gliese:
                name = 'Gliese: {0}'.format(self.gliese)
            elif self.HIP:
                name = 'HIP: {0}'.format(self.HIP)
            elif self.HD:
                name = 'HD: {0}'.format(self.HD)
            else:
                name = 'Star: {0}'.format(self.id)
        return name

    class Meta:
        verbose_name_plural = 'Stars in the Galaxy'
        ordering = ['distance_parsecs']

class Planet(models.Model):
    """
    Current version imported from the exoplanets table: http://exoplanets.org/table
    Added specific field names, and removed others
    Use these fields: NAME,MSINI,A,PER,ECC,OM,T0,K,OTHERNAME,HD,HR,HIPP,GL,KEPID,R,DENSITY,GRAVITY
    -- Remove second line of CSV that has subtitles
    -- Add a new column at beginning that has ids of ascending numbers
    """
    name = models.CharField(max_length=60, help_text="Planet Common Name", blank=True, null=True)
    mass = models.FloatField(help_text="Estimated Mass compared to Jupiter", blank=True, null=True)
    semi_major_axis = models.FloatField(help_text="Semi-major Axis in au", blank=True, null=True)
    orbital_period = models.FloatField(help_text="Orbital Period in days", blank=True, null=True)
    orbital_eccentricity = models.FloatField(help_text="Orbital Eccentricity", blank=True, null=True)
    periastron = models.FloatField(help_text="Degrees of Periastron", blank=True, null=True)
    periastron_time = models.FloatField(help_text="Time of Periastron in JD", blank=True, null=True)
    velocity_semi_amplitude = models.FloatField(help_text="Semiamplitude of doppler variation", blank=True, null=True)
    other_name = models.CharField(max_length=60, help_text="Alternate Planet Common Name", blank=True, null=True)
    HD = models.PositiveIntegerField(help_text="The star's ID in the Henry Draper catalog, if known.", blank=True, null=True)
    HR = models.PositiveIntegerField(help_text="The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.", blank=True, null=True)
    HIPP = models.PositiveIntegerField(help_text="The star's ID in the Hipparcos catalog, if known.", blank=True, null=True)
    gliese = models.CharField(max_length=40, help_text="The star's ID in the third edition of the Gliese Catalog of Nearby Stars.", blank=True, null=True)
    kepler_id = models.CharField(max_length=40, help_text="The star's Kepler ID.", blank=True, null=True)
    radius = models.FloatField(help_text="Radius in jupiters", blank=True, null=True)
    density = models.FloatField(help_text="Density in g/cm^3", blank=True, null=True)
    gravity = models.FloatField(help_text="Surface Gravity", blank=True, null=True)

    def __unicode__(self):
        name = self.name
        if self.other_name:
            name = '{0} [{1}]'.format(self.name, self.other_name)
        return name

    class Meta:
        verbose_name_plural = 'Known Planets'
        ordering = ['name']