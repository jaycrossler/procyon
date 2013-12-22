from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from procyon.starsystemmaker.space_helpers import *

from django.contrib.gis.db import models
from procyon.starcatalog.models import Star, StarType, StarLuminosityType
import json

class StarModel(models.Model):
    """
    Additional data and simulated info about stars.
    Data needs to be generated using 'build_model' before being accessed
    """

    star = models.OneToOneField(Star, db_index=True, help_text="The star with real data", default=1)
    star_type = models.ForeignKey(StarType, help_text="Stellar Classification", blank=True, null=True)
    luminosity_class = models.ForeignKey(StarLuminosityType, help_text="Luminosity Class (0-VII)", blank=True, null=True)
    luminosity_mod = models.CharField(max_length=5, help_text="Luminosity sub class (a, ab, b, a-0", blank=True, null=True)
    base_color = models.CharField(max_length=8, help_text="Basic RBG Color", default="#ffddbe", blank=True, null=True)

    rand_seed = models.FloatField(help_text="Random Seed from 0-1 used to build notional system", blank=True, null=True, default=0)
    guessed_temp = models.FloatField(help_text="Guessed at Temperature", blank=True, null=True, default=0)
    guessed_mass = models.FloatField(help_text="Guessed at Mass", blank=True, null=True, default=0)
    guessed_radius = models.FloatField(help_text="Guessed at Radius", blank=True, null=True, default=0)
    guessed_age = models.FloatField(help_text="Guessed at Age", blank=True, null=True, default=0)

    json_of_closest_stars = models.TextField(help_text="List of Stars, will be filled in automatically on first calculation", blank=True, null=True)

    ids_of_companion_stars = models.CharField(max_length=30, help_text="Comma-separated IDs of any stars within .3 LY", blank=True, null=True)

    location = models.PointField(db_index=True, dim=3, blank=True, null=True, srid=900913)
    objects = models.GeoManager()

    def build_model(self, star_id=None, star_prime=None, forced=False):
        np.random.seed()

        self.add_rand_seed(forced)

        if not star_prime and not star_id:
            star_prime = self.star

        if star_prime:
            self.star = star_prime
        else:
            self.star = Star.objects.get(id=star_id)
        if self.star:
            star_a, star_b, star_c, star_d = get_star_type(self.star.spectrum)
            self.add_type(star_a)
            self.add_color(star_a, star_b, star_c)
            self.add_luminosity(star_c)
            self.luminosity_mod = star_d

        self.add_rand_variables(forced)

        self.save()

    def add_rand_seed(self, forced=False):
        add_it = True
        if not forced and self.rand_seed:
            add_it = False
        if add_it:
            self.rand_seed = np.random.random() #rand_range(0, 1)
            self.save()

    def add_rand_variables(self, forced=False):
        add_it = True
        if not forced and self.guessed_temp:
            add_it = False
        if add_it:
            options = {'rand_seed': self.rand_seed, 'star_type': self.star_type,
                       'temp': 0, 'mass': 0, 'age': 0, 'radius': 0,
                       'luminosity_class': self.luminosity_class, 'luminosity_mod': self.luminosity_mod}

            settings = star_variables(options)

            self.guessed_temp = settings.get('temp', 0)
            self.guessed_mass = settings.get('mass', 0)
            self.guessed_radius = settings.get('radius', 0)
            self.guessed_age = settings.get('age', 0)
            self.save()

    def add_luminosity(self, star_c):
        result = "ok"
        try:
            star_type = StarLuminosityType.objects.get(symbol=star_c)
            self.luminosity_class = star_type
        except StarLuminosityType.DoesNotExist:
            result = "unknown"
        return result

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
        verbose_name_plural = 'Stars (Simulated)'
        ordering = ['star']

    def nearby_stars(self, force_regenerate=False):
        if self.json_of_closest_stars and not force_regenerate:
            star_list = json.loads(self.json_of_closest_stars)
        else:
            star_list = closest_stars(self, StarModel)
            self.json_of_closest_stars = json.dumps(star_list)
            self.save()

        return star_list

    def nearby_stars_json(self):
        self.nearby_stars()
        return self.json_of_closest_stars

    def nearby_stars_json_force_recalc(self):
        self.nearby_stars(force_regenerate=True)
        return self.json_of_closest_stars

    additional_methods = ['nearby_stars', ]

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
            val = self.__getattribute__(field)
            if type(val) == Point:
                point = dict()
                point['x'] = val.x
                point['y'] = val.y
                point['z'] = val.z
                dumps[str(field)] = point
            else:
                dumps[str(field)] = str(val)
        for func in additional_methods:
            dumps[func] = getattr(self, func)()
        return dumps


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


class PlanetFeature(models.Model):
    """
    Major features of a planetary body
    """
    short_name = models.CharField(db_index=True, max_length=60, help_text="Short Description of Planetary Feature", blank=True, null=True)
    details = models.TextField(help_text="Detailed Description of Planetary Feature", blank=True, null=True)
    rules_required = models.TextField(help_text="What attributes of the planet must be true to have this feature?", blank=True, null=True)
    rules_more_likely = models.TextField(help_text="What attributes of the planet double the chances to have this feature?", blank=True, null=True)
    likelihood = models.FloatField(help_text="How likely is a planet to have this feature (0 to 1) given that the above are met?", blank=True, null=True, default="0.1")


class PlanetModel(models.Model):
    """
    Simulated Planets
    """
    name = models.CharField(db_index=True, max_length=60, help_text="Planet Common Name", blank=True, null=True)
    planet_type = models.ForeignKey(PlanetType, help_text="Type of planet", default=1, blank=True, null=True)

    mass = models.FloatField(db_index=True, help_text="Estimated Mass (Earth=1, Mercury=.05, Mars=.1, Jupiter=317)", blank=True, null=True)
    radius = models.FloatField(help_text="Estimated Radius (Earth=1, Mercury=.382, Jupiter=10.97, Saturn=9.14) ", blank=True, null=True)
    density = models.FloatField(help_text="Density in g/cm^3 (Earth=5.51, Jupiter=1.33, Saturn=0.68, Pluto=1.75)", blank=True, null=True)
    gravity = models.FloatField(help_text="Surface Gravity (g=m/r^2, Earth=1, Mercury=0.38, Jupiter=2.53, Pluto=0.067)", blank=True, null=True)

    oblateness = models.FloatField(help_text="How squished it is (Earth=.0034, Venus=0, Saturn=.0979)", blank=True, null=True)
    tilt = models.FloatField(help_text="Axial Tilt (Earth=23.4, Uranus=97, Venus=177)", blank=True, null=True)
    albedo = models.FloatField(help_text="How much light does the surface reflect (0 to 1)", blank=True, null=True)

    length_days = models.FloatField(help_text="How many hours are the days (Earth=24)", blank=True, null=True)
    surface_temp_low = models.CharField(max_length=30, help_text="Low Temperature in C", blank=True, null=True, default=0)
    surface_temp_high = models.CharField(max_length=30, help_text="Low Temperature in C", blank=True, null=True, default=0)
    magnetic_field = models.FloatField(help_text="How strong a magnetic field (Earth=1, Jupiter=19519)", blank=True, null=True)
    craterization = models.FloatField(help_text="How many craters? (Earth=1, Moon=2, Mars=3, Jupiter=0)", blank=True, null=True)

    #TODO: Figure out how to have a list of minerals and amounts that makes sense for coloring, mining, changing
    #TODO: Same for atmosphere gasses
    mineral_surface_early = models.FloatField(help_text="% Amount of H, He, C (0 to 1)", blank=True, null=True)
    mineral_surface_mid = models.FloatField(help_text="% Amount of N, O, Fe (0 to 1)", blank=True, null=True)
    mineral_surface_heavy = models.FloatField(help_text="% Amount of Heavier Metals (0 to 1)", blank=True, null=True)
    mineral_surface_late = models.FloatField(help_text="% Amount of Exotic Metals (0 to 1)", blank=True, null=True)
    minerals_specific = models.CharField(max_length=100, help_text="Comma-separated list of specific notable minerals", blank=True, null=True, default="")

    solid_core_size = models.FloatField(help_text="Percentage size of planet that is core (0 to 1, Earth=.31)", blank=True, null=True)
    solid_core_type = models.CharField(max_length=30, help_text="Type of Core", blank=True, null=True, default="Iron")
    plate_tectonics_amount = models.FloatField(help_text="Amount of tectonics and plate movement (Earth=1, Io=20)", blank=True, null=True)

    surface_solidity = models.FloatField(help_text="How solid is surface (Inner=1, Gas Giants=0)", blank=True, null=True)
    surface_ocean_amount = models.FloatField(help_text="% surface is covered with liquid (0 to 1, Earth=.71)", blank=True, null=True)
    surface_ocean_chemicals = models.CharField(max_length=100, help_text="Main composition of surface oceans (Earth=Salt Water, Titan=Ethane and Methane", blank=True, null=True, default="")
    subsurface_ocean_amount = models.FloatField(help_text="% of subsurface that is liquid (0 to 1, Europa=1.0)", blank=True, null=True)

    ice_amount_north_pole = models.FloatField(help_text="% North Pole is covered with ice (0 to 1, Earth=.01)", blank=True, null=True)
    ice_amount_south_pole = models.FloatField(help_text="% South Pole is covered with ice (0 to 1, Earth=.01)", blank=True, null=True)
    ice_amount_total = models.FloatField(help_text="% overall surface is covered with ice, not counting poles (0 to 1, Europa=1.0)", blank=True, null=True)

    semi_major_axis = models.FloatField(help_text="Semi-major Axis in au", blank=True, null=True)
    revolution = models.FloatField(help_text="Revolutions per earth day", blank=True, null=True)
    orbital_period = models.FloatField(help_text="Orbital Period in days", blank=True, null=True)
    orbital_eccentricity = models.FloatField(help_text="Orbital Eccentricity", blank=True, null=True)
    periastron = models.FloatField(help_text="Degrees of Periastron", blank=True, null=True)
    periastron_time = models.FloatField(help_text="Time of Periastron in JD", blank=True, null=True)
    velocity_semi_amplitude = models.FloatField(help_text="Semiamplitude of doppler variation", blank=True, null=True)

    ring_size = models.FloatField(help_text="Size of rings (as percentage of radius)", blank=True, null=True)
    ring_numbers = models.IntegerField(help_text="Number of ring groups", blank=True, null=True)

    atmosphere_millibars = models.FloatField(help_text="Pressure of atmosphere in Millibars (Mars=7, Earth=1013.25)", blank=True, null=True)
    atmosphere_main_gas = models.CharField(max_length=30, help_text="Major gas (70%), if any", blank=True, null=True)
    atmosphere_secondary_gas = models.CharField(max_length=30, help_text="Second gas (20%), if any", blank=True, null=True)
    atmosphere_tertiary_gas = models.CharField(max_length=30, help_text="Tertiary gas (9%), if any", blank=True, null=True)
    atmosphere_dust_amount = models.FloatField(help_text="Grams of dust/m^2 (Earth=1, Moon=1000, Mars=500)", blank=True, null=True)

    surface_wind_speeds_avg = models.FloatField(help_text="Average Wind Speeds in km/hr (Mars=108, Earth=17, Neptune=700)", blank=True, null=True)
    surface_wind_speeds_max = models.FloatField(help_text="Max Wind Speeds in km/hr (Mars=288, Earth=400, Neptune=2100)", blank=True, null=True)

    other_name = models.CharField(db_index=True, max_length=60, help_text="Alternate Planet Common Name", blank=True, null=True)
    parent_star = models.ForeignKey(Star, db_index=True, help_text="The star that it orbits", blank=True, null=True)
    parent_planet = models.ForeignKey('self', db_index=True, help_text="A planet that it orbits",  blank=True, null=True)

    major_features = models.ManyToManyField(PlanetFeature, help_text="What features are significant on this planet", blank=True, null=True)

    def __unicode__(self):
        name = self.name
        if self.other_name:
            name = '{0} [{1}]'.format(self.name, self.other_name)
        return name

    class Meta:
        verbose_name_plural = 'Planets (Simulated)'
        ordering = ['name']

    additional_methods = ['__unicode__', ]

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