from procyon.starsystemmaker.space_helpers import *
from django.contrib.gis.db import models
from procyon.starcatalog.models import Star, StarType


class StarModel(models.Model):
    """
    Additional data and simulated info about stars.
    Data needs to be generated using 'build_model' before being accessed

    TODO: Build getter that generates info if not yet created
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

    def build_model(self, star_id, star_prime=None):
        #TODO: If not star_id, search through stars and find one
        self.add_rand_seed(True)
        if star_prime:
            self.star = star_prime
        else:
            self.star = Star.objects.get(id=star_id)
        if self.star:
            star_a, star_b, star_c = get_star_type(self.star.spectrum)
            self.add_type(star_a)
            self.add_color(star_a, star_b, star_c)

        self.add_rand_variables(True)

        self.save()

    def add_rand_seed(self, forced=False):
        add_it = True
        if not forced and self.rand_seed:
            add_it = False
        if add_it:
            self.rand_seed = rand_range(0, 1)
            self.save()

    def add_rand_variables(self, forced=False):
        #TODO: How to use the Rand Seed as the proper seed variable so that all numbers are derived from that?
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

    def get_params(self):
        """
        Converts parameters to object.
        """
        additional_methods = []
        dumps = dict()
        model_fields = [field.name for field in self._meta.fields]

        for field in model_fields:
            dumps[str(field)] = str(self.__getattribute__(field))
        for func in additional_methods:
            dumps[func] = str(getattr(self, func)())
        return dumps

    class Meta:
        verbose_name_plural = 'Stars (Simulated)'
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
    magnetic_field_range = models.CharField(max_length=30, help_text="Amount of magnetic field, 0 for none. (Earth=1, Jupiter=19519)", blank=True, null=True, default=0)
    craterization_range = models.CharField(max_length=30, help_text="Amount of surface bombardment, 0 for none. (Earth=1)", blank=True, null=True, default=0)

    mineral_surface = models.BooleanField(help_text="Is surface made of rock?", blank=True)
    solid_core = models.BooleanField(help_text="Is core solid?", blank=True)
    plate_tectonics = models.BooleanField(help_text="Is surface made of moving plates?", blank=True)

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Types of Planets'


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

    inclination = models.FloatField(help_text="Inclination", blank=True, null=True)
    oblateness = models.FloatField(help_text="How squished it is", blank=True, null=True)
    tilt = models.FloatField(help_text="Tilt", blank=True, null=True)
    albedo = models.FloatField(help_text="How bright it is (0 to 1)", blank=True, null=True)

    length_days = models.FloatField(help_text="How squished it is", blank=True, null=True)
    surface_temperature_range = models.CharField(max_length=30, help_text="Range in C", blank=True, null=True, default=0)
    magnetic_field = models.FloatField(help_text="How strong a magnetic field (Earth=1, Jupiter=19519)", blank=True, null=True)
    craterization = models.FloatField(help_text="How many craters? (Earth=1)", blank=True, null=True)

    mineral_surface_early = models.FloatField(help_text="% Amount of H, He, C (0 to 1)", blank=True, null=True)
    mineral_surface_mid = models.FloatField(help_text="% Amount of N, O (0 to 1)", blank=True, null=True)
    mineral_surface_heavy = models.FloatField(help_text="% Amount of Heavier Metals (0 to 1)", blank=True, null=True)
    mineral_surface_late = models.FloatField(help_text="% Amount of Exotic Metals (0 to 1)", blank=True, null=True)
    minerals_specific = models.CharField(max_length=100, help_text="Comma-separated list of specific notable minerals", blank=True, null=True, default="")

    solid_core_size = models.FloatField(help_text="Percentage size of planet that is core (0 to 1)", blank=True, null=True)
    solid_corex_type = models.CharField(max_length=30, help_text="Type of Core", blank=True, null=True, default="Iron")
    plate_tectonics_amount = models.FloatField(help_text="Amount of tectonics and plate movement (Earth=1, Io=20)", blank=True, null=True)

    surface_ocean_amount = models.FloatField(help_text="% surface is covered with water (0 to 1)", blank=True, null=True)
    subsurface_ocean_amount = models.FloatField(help_text="% of subsurface that is water (0 to 1)", blank=True, null=True)
    ice_amount = models.FloatField(help_text="% surface is covered with ice (0 to 1)", blank=True, null=True)

    semi_major_axis = models.FloatField(help_text="Semi-major Axis in au", blank=True, null=True)
    revolution = models.FloatField(help_text="Revolutions per earth day", blank=True, null=True)
    orbital_period = models.FloatField(help_text="Orbital Period in days", blank=True, null=True)
    orbital_eccentricity = models.FloatField(help_text="Orbital Eccentricity", blank=True, null=True)
    periastron = models.FloatField(help_text="Degrees of Periastron", blank=True, null=True)
    periastron_time = models.FloatField(help_text="Time of Periastron in JD", blank=True, null=True)
    velocity_semi_amplitude = models.FloatField(help_text="Semiamplitude of doppler variation", blank=True, null=True)

    other_name = models.CharField(db_index=True, max_length=60, help_text="Alternate Planet Common Name", blank=True, null=True)
    parent_star = models.ForeignKey(Star, db_index=True, help_text="The star that it orbits", blank=True, null=True)
    parent_planet = models.ForeignKey('self', db_index=True, help_text="A planet that it orbits",  blank=True, null=True)

    def __unicode__(self):
        name = self.name
        if self.other_name:
            name = '{0} [{1}]'.format(self.name, self.other_name)
        return name

    class Meta:
        verbose_name_plural = 'Planets (Simulated)'
        ordering = ['name']
