from django.contrib.gis.db import models
from procyon.starsystemmaker.space_helpers import *
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

    class Meta:
        verbose_name_plural = 'Stellar Classifications'


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

    #TODO: List all known planets
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
        verbose_name_plural = 'Official Star Data'
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
                planet_list.append(p)
        if self.HR:
            planets = Planet.objects.filter(HD=self.HR)
            for p in planets.all():
                planet_list.append(p)
        if self.gliese:
            planets = Planet.objects.filter(gliese=self.gliese)
            for p in planets.all():
                planet_list.append(p)

        return planet_list

    def create_star_model(self, force=False):
        status = "exists"
        star_model, created = StarModel.objects.get_or_create(star=self)
        if created or force:
            star_model.build_model()
            status = "built"
        star_model.save()
        return status

    def known_planet_count(self):
        return len(self.known_planets())

    def distance_ly(self):
        return float(self.distance_parsecs) * 3.26163344

    def possibly_habitable(self):
        result = False
        if self.HIP:
            result = StarPossiblyHabitable.objects.filter(HIP=self.HIP).exists()
        return result

    def web_color(self):
        star_a, star_b, star_c = get_star_type(self.spectrum)
        return color_of_star(star_a, star_b, star_c)


class Planet(models.Model):
    """
    Current version imported from the exoplanets table: http://exoplanets.org/table
    Added specific field names, and removed others
    Use these fields: NAME,MSINI,A,PER,ECC,OM,T0,K,OTHERNAME,HD,HR,HIPP,GL,KEPID,R,DENSITY,GRAVITY
    -- Remove second line of CSV that has subtitles
    -- Add a new column at beginning that has ids of ascending numbers
    """
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

    class Meta:
        verbose_name_plural = 'Known Planets'
        ordering = ['name']


class StarModel(models.Model):
    """
    Additional data and simulated info about stars.
    Data will be generated through a long-running task

    TODO: Maybe should move to systemmaker?
    """
    star = models.OneToOneField(Star, db_index=True, help_text="The star with real data", default=1)
    star_type = models.ForeignKey(StarType, help_text="Stellar Classification", blank=True, null=True)
    base_color = models.CharField(max_length=8, help_text="Basic RBG Color", default="#ffddbe", blank=True, null=True)

    rand_seed = models.FloatField(help_text="Random Seed from 0-1 used to build notional system", blank=True, null=True, default=0)
    guessed_temp = models.FloatField(help_text="Guessed at Temperature", blank=True, null=True, default=0)
    guessed_mass = models.FloatField(help_text="Guessed at Mass", blank=True, null=True, default=0)
    guessed_radius = models.FloatField(help_text="Guessed at Radius", blank=True, null=True, default=0)
    guessed_luminosity = models.FloatField(help_text="Guessed at Luminosity", blank=True, null=True, default=0)
    guessed_age = models.FloatField(help_text="Guessed at Age", blank=True, null=True, default=0)

    def build_model(self):
        self.add_rand_seed(True)
        self.add_rand_variables(True)

        star_a, star_b, star_c = get_star_type(self.star.spectrum)
        self.add_type(star_a)
        self.add_color(star_a, star_b, star_c)

    def add_rand_seed(self, forced=False):
        add_it = True
        if not forced and self.rand_seed:
            add_it = False
        if add_it:
            self.rand_seed = rand_range(0, 1)
            self.save()

    def add_rand_variables(self, forced=False):
        #TODO: How to use the Rand Seed as the proper seed variable?
        add_it = True
        if not forced and self.guessed_temp:
            add_it = False
        if add_it:
            star_type = self.star_type
            if star_type:
                self.guessed_temp = rand_range_from_text(star_type.surface_temp_range)
                self.guessed_mass = rand_range_from_text(star_type.mass_range)
                self.guessed_radius = rand_range_from_text(star_type.radius_range)
                self.guessed_luminosity = rand_range_from_text(star_type.luminosity_range)
                self.guessed_age = rand_range_from_text(star_type.age)
                self.save()

    def add_type(self, star_a):
        result = "ok"
        try:
            star_type = StarType.objects.get(symbol=star_a)
            self.star_type = star_type
        except StarType.DoesNotExist:
            result = "unknown"
        return result

    def add_color(self, star_a="K", star_b="", star_c=""):
        star = self
        found_color = ""
        if star_a or star_b or star_c:
            found_color = color_of_star(star_a, star_b, star_c)
        if not found_color and star.star and star.star.spectrum:
            star_a, star_b, star_c = get_star_type(star.star.spectrum)
            found_color = color_of_star(star_a, star_b, star_c)
        if not found_color:
            if star.star_type and star.star_type.base_color:
                found_color = star.star_type.base_color
        star.base_color = found_color
        star.save()

    class Meta:
        verbose_name_plural = 'Stars in the galaxy'
        ordering = ['star']


class PlanetType(models.Model):
    """
    Planet Types (from http://en.wikipedia.org/wiki/List_of_planet_types)
    """
    name = models.CharField(max_length=30, help_text="Short description", blank=True, null=True)
    mass_range = models.CharField(max_length=30, help_text="Mass Range in sextillion tonnes (10^24. Earth=5.9)", blank=True, null=True)
    radius_range = models.CharField(max_length=30, help_text="Radius Range in km (Earth=6371)", blank=True, null=True)
    age_range = models.CharField(max_length=30, help_text="Age Range in million years (Earth=4540)", blank=True, null=True)
    surface_area_range = models.CharField(max_length=30, help_text="Surface Area Range in million km^2 (Earth=510.1)", blank=True, null=True)
    moon_range = models.CharField(max_length=30, help_text="Average number of moons (Earth=1)", blank=True, null=True)
    density_range = models.CharField(max_length=30, help_text="Density Range in % (Earth=1)", blank=True, null=True)
    length_days_range = models.CharField(max_length=30, help_text="Day Length Range in hours (Earth=24)", blank=True, null=True)
    temperature_range = models.CharField(max_length=30, help_text="Temperature Range in C (Earth=15)", blank=True, null=True)
    magnetic_field_range = models.CharField(max_length=30, help_text="Amount of magnetic field, 0 for none. (Earth=1)", blank=True, null=True, default=0)
    craterization_range = models.CharField(max_length=30, help_text="Amount of surface bombardment, 0 for none. (Earth=1)", blank=True, null=True, default=0)

    mineral_surface = models.BooleanField(help_text="Is surface made of rock?", blank=True)
    solid_core = models.BooleanField(help_text="Is core solid?", blank=True)
    plate_tectonics = models.BooleanField(help_text="Is surface made of moving plates?", blank=True)

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Planet Classifications'


class PlanetModel(models.Model):
    """
    Simulated Planets
    """
    name = models.CharField(db_index=True, max_length=60, help_text="Planet Common Name", blank=True, null=True)
    planet_type = models.ForeignKey(PlanetType, help_text="Type of planet", default=1, blank=True, null=True)

    mass = models.FloatField(db_index=True, help_text="Estimated Mass compared to Jupiter", blank=True, null=True)
    radius = models.FloatField(help_text="Radius in jupiters", blank=True, null=True)
    density = models.FloatField(help_text="Density in g/cm^3", blank=True, null=True)
    gravity = models.FloatField(help_text="Surface Gravity", blank=True, null=True)

    semi_major_axis = models.FloatField(help_text="Semi-major Axis in au", blank=True, null=True)
    orbital_period = models.FloatField(help_text="Orbital Period in days", blank=True, null=True)
    orbital_eccentricity = models.FloatField(help_text="Orbital Eccentricity", blank=True, null=True)
    periastron = models.FloatField(help_text="Degrees of Periastron", blank=True, null=True)
    periastron_time = models.FloatField(help_text="Time of Periastron in JD", blank=True, null=True)
    velocity_semi_amplitude = models.FloatField(help_text="Semiamplitude of doppler variation", blank=True, null=True)
    other_name = models.CharField(db_index=True, max_length=60, help_text="Alternate Planet Common Name", blank=True, null=True)
    star = models.ForeignKey(Star, db_index=True, help_text="The star with real data", default=1, blank=True, null=True)

    def __unicode__(self):
        name = self.name
        if self.other_name:
            name = '{0} [{1}]'.format(self.name, self.other_name)
        return name

    class Meta:
        verbose_name_plural = 'Simluated Planets'
        ordering = ['name']
