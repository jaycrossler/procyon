from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from procyon.starsystemmaker.space_helpers import *
from django.contrib.gis.db import models
import json


class StarPossiblyHabitable(models.Model):
    """
    Extracted from HabHYG at: http://www.projectrho.com/public_html/starmaps/supplement/HabHYG.zip
    """
    HIP = models.PositiveIntegerField(db_index=True, help_text="Hipparcos Catalog number of Potentially Habitable System", blank=True, null=True)


class StarType(models.Model):
    """
    Stellar Types (from Morgan-Keenan Main Sequence types)
    """
    symbol = models.CharField(db_index=True, max_length=2, help_text="Morgan-Keenan Main Sequence Symbol", default="K")
    name = models.CharField(max_length=30, help_text="Short description", blank=True, null=True)
    description = models.TextField(help_text="Details", blank=True, null=True)
    surface_temp_range = models.CharField(max_length=30, help_text="Temp Range in K (eg 2000-5000)", blank=True, null=True)
    base_color = models.CharField(max_length=8, help_text="Basic RBG Color", default="#ffddbe", blank=True, null=True)
    mass_range = models.CharField(max_length=30, help_text="Mass Range compared to Sol", blank=True, null=True)
    radius_range = models.CharField(max_length=30, help_text="Radius Range compared to Sol", blank=True, null=True)
    luminosity_range = models.CharField(max_length=30, help_text="Luminosity Range compared to Sol", blank=True, null=True)
    age = models.CharField(max_length=30, help_text="Approx Age in Millions of Years of a Type V star", blank=True, null=True, default="5300")

    def __unicode__(self):
        return '{0}: {1}'.format(self.symbol, self.name)

    additional_methods = ['__unicode__', ]

    def get_params(self, requested_methods=None):
        """
        Converts parameters to object.
        """
        additional_methods = self.additional_methods

        if requested_methods:
            additional_methods = requested_methods + additional_methods
        dumps = dict()
        model_fields = [field.name for field in self._meta.fields]

        for field in model_fields:
            dumps[str(field)] = str(self.__getattribute__(field))
        for func in additional_methods:
            dumps[func] = str(getattr(self, func)())
        return dumps

    def get_json(self):
        return json.dumps(self.get_params(), ensure_ascii=True)

    class Meta:
        verbose_name_plural = 'Types of Stars'


class Star(models.Model):
    """
    It's full of stars. (Mainly Hipparcos, Yale Bright Star, ana Gilese catalog stars within 50 parsecs)
    Current version imported from the HYG Stellar database http://www.astronexus.com/node/34
    CSV maintained at https://github.com/astronexus/HYG-Database/blob/master/hygfull.csv
    """
    HIP = models.PositiveIntegerField(db_index=True, help_text="Hipparcos Catalog number", blank=True, null=True)
    HD = models.PositiveIntegerField(db_index=True, help_text="The star's ID in the Henry Draper catalog, if known.", blank=True, null=True)
    HR = models.PositiveIntegerField(db_index=True, help_text="The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.", blank=True, null=True)
    gliese = models.CharField(db_index=True, max_length=40, help_text="The star's ID in the third edition of the Gliese Catalog of Nearby Stars.", blank=True, null=True)
    bayer_flamsteed = models.CharField(max_length=40, help_text="The Bayer / Flamsteed designation, from the Fifth Edition of the Yale Bright Star Catalog. This is a combination of the two designations. The Flamsteed number, if present, is given first; then a three-letter abbreviation for the Bayer Greek letter; the Bayer superscript number, if present; and finally, the three-letter constellation abbreviation. Thus Alpha Andromedae has the field value '21Alp And', and Kappa1 Sculptoris (no Flamsteed number) has 'Kap1Scl'.", blank=True, null=True)
    proper_name = models.CharField(db_index=True, max_length=100, help_text="A common name for the star", blank=True, null=True)
    RA = models.FloatField(help_text="The star's right ascension for epoch 2000.0", blank=True, null=True)
    dec = models.FloatField(help_text="The star's right declination for epoch 2000.0", blank=True, null=True)
    distance_parsecs = models.FloatField(db_index=True, help_text="Distance in Parsecs, (Light Years * 4.3)", blank=True, null=True)
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
    VX = models.FloatField(help_text="Annual parsec change in Galactic X Coordinate", blank=True, null=True)
    VY = models.FloatField(help_text="Annual parsec change in Galactic Y Coordinate", blank=True, null=True)
    VZ = models.FloatField(help_text="Annual parsec change in Galactic Z Coordinate", blank=True, null=True)

    #TODO: Generate notional planetary system using known planets
    #TODO: When searching, list nearest stars and planets

    def __unicode__(self):
        name = self.proper_name
        if not name:
            if self.bayer_flamsteed:
                name = self.bayer_flamsteed
            elif self.HD:
                name = 'HD: {0}'.format(self.HD)
            elif self.HR:
                name = 'HR: {0}'.format(self.HR)
            elif self.gliese:
                name = 'Gliese: {0}'.format(self.gliese)
            elif self.HIP:
                name = 'HIP: {0}'.format(self.HIP)
            else:
                name = 'Star: {0}'.format(self.id)
        return name

    class Meta:
        verbose_name_plural = 'Stars'
        ordering = ['distance_parsecs']

    def known_planets(self):
        """
        Returns a list of all related planets.
        """
        planet_list = []
        if self.HIP:
            planets = Planet.objects.filter(HIP=self.HIP)
            for p in planets.all():
                planet_list.append(p)
        if self.HD:
            planets = Planet.objects.filter(HD=self.HD)
            for p in planets.all():
                if p not in planet_list:
                    planet_list.append(p)
        if self.HR:
            planets = Planet.objects.filter(HD=self.HR)
            for p in planets.all():
                if p not in planet_list:
                    planet_list.append(p)
        if self.gliese:
            planets = Planet.objects.filter(gliese=self.gliese)
            for p in planets.all():
                if p not in planet_list:
                    planet_list.append(p)

        results = []
        for p in planet_list:
            results.append(p.get_params())
        return results

    def known_planet_count(self):
        return len(self.known_planets())

    def distance_ly(self):
        ly = float(self.distance_parsecs) * 3.26163344
        ly = round(ly, 2)
        return ly

    def possibly_habitable(self):
        result = False
        if self.HIP:
            result = StarPossiblyHabitable.objects.filter(HIP=self.HIP).exists()
        return result

    def web_color(self):
        star_a, star_b, star_c = get_star_type(self.spectrum)
        return color_of_star(star_a, star_b, star_c)

    def nearby_stars(self):
        star_list = []

        origin = Point(self.X, self.Y, self.Z)

        distance = 100
        #Something like: Star.objects.filter(point__distance_lte=(origin, D(m=distance))).distance(origin).order_by('distance')[:1][20]

        for s in Star.objects.filter(id__lte=5):
            star_handle = dict()
            star_handle['name'] = s.__unicode__()
            star_handle['id'] = s.id
            star_handle['web_color'] = s.web_color()
            star_handle['x']= s.X
            star_handle['y'] = s.Y
            star_handle['z'] = s.Z
            star_list.append(star_handle)

        return star_list

    additional_methods = ['known_planet_count', 'possibly_habitable', 'web_color', '__unicode__', 'known_planets', ]

    def get_params(self, requested_methods=None, only_variables=None):
        """
        Converts parameters to object.

        Options:
            requested_methods = ['__unicode__', ] (to also call these functions and return results)
            only_variables = ['name', 'title', ] (to only return values of these model variables)

        """
        additional_methods = self.additional_methods

        if requested_methods:
            additional_methods = requested_methods + additional_methods
        dumps = dict()

        if not only_variables:
            model_fields = [field.name for field in self._meta.fields]
        else:
            model_fields = only_variables

        for field in model_fields:
            dumps[str(field)] = str(self.__getattribute__(field))
        for func in additional_methods:
            dumps[func] = getattr(self, func)()
        return dumps

    def get_json(self):
        return json.dumps(self.get_params(), ensure_ascii=True)


class Planet(models.Model):
    """
    Current version imported from the exoplanets table: http://exoplanets.org/table
    Added specific field names, and removed others
    Use these fields: NAME,MSINI,A,PER,ECC,OM,T0,K,OTHERNAME,HD,HR,HIPP,GL,KEPID,R,DENSITY,GRAVITY
    -- Remove second line of CSV that has subtitles
    -- Add a new column at beginning that has ids of ascending numbers
    """
    additional_methods = ['__unicode__', ]

    name = models.CharField(db_index=True, max_length=60, help_text="Planet Common Name", blank=True, null=True)
    mass = models.FloatField(db_index=True, help_text="Estimated Mass compared to Jupiter", blank=True, null=True)
    semi_major_axis = models.FloatField(help_text="Semi-major Axis in au", blank=True, null=True)
    orbital_period = models.FloatField(help_text="Orbital Period in days", blank=True, null=True)
    orbital_eccentricity = models.FloatField(help_text="Orbital Eccentricity", blank=True, null=True)
    periastron = models.FloatField(help_text="Degrees of Periastron", blank=True, null=True)
    periastron_time = models.FloatField(help_text="Time of Periastron in JD", blank=True, null=True)
    velocity_semi_amplitude = models.FloatField(help_text="Semiamplitude of doppler variation", blank=True, null=True)
    other_name = models.CharField(db_index=True, max_length=60, help_text="Alternate Planet Common Name", blank=True, null=True)
    HD = models.PositiveIntegerField(db_index=True, help_text="The star's ID in the Henry Draper catalog, if known.", blank=True, null=True)
    HR = models.PositiveIntegerField(db_index=True, help_text="The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.", blank=True, null=True)
    HIP = models.PositiveIntegerField(db_index=True, help_text="The star's ID in the Hipparcos catalog, if known.", blank=True, null=True)
    gliese = models.CharField(db_index=True, max_length=40, help_text="The star's ID in the third edition of the Gliese Catalog of Nearby Stars.", blank=True, null=True)
    kepler_id = models.CharField(db_index=True, max_length=40, help_text="The star's Kepler ID.", blank=True, null=True)
    radius = models.FloatField(help_text="Radius in jupiters", blank=True, null=True)
    density = models.FloatField(help_text="Density in g/cm^3", blank=True, null=True)
    gravity = models.FloatField(help_text="Surface Gravity", blank=True, null=True)

    def __unicode__(self):
        name = self.name
        if self.other_name:
            name = '{0} [{1}]'.format(self.name, self.other_name)
        return name

    def get_params(self, requested_methods=None, only_variables=None):
        """
        Converts parameters to object.

        Options:
            requested_methods = ['__unicode__', ] (to also call these functions and return results)
            only_variables = ['name', 'title', ] (to only return values of these model variables)

        """
        additional_methods = self.additional_methods

        if requested_methods:
            additional_methods = requested_methods + additional_methods
        dumps = dict()

        if not only_variables:
            model_fields = [field.name for field in self._meta.fields]
        else:
            model_fields = only_variables

        for field in model_fields:
            dumps[str(field)] = str(self.__getattribute__(field))
        for func in additional_methods:
            dumps[func] = getattr(self, func)()
        return dumps

    def get_json(self):
        return json.dumps(self.get_params(), ensure_ascii=True)

    class Meta:
        verbose_name_plural = 'Planets (Discovered)'
        ordering = ['name']


