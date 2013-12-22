# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PlanetModel.surface_temperature_range'
        db.delete_column(u'starsystemmaker_planetmodel', 'surface_temperature_range')

        # Deleting field 'PlanetModel.ice_amount'
        db.delete_column(u'starsystemmaker_planetmodel', 'ice_amount')

        # Adding field 'PlanetModel.surface_temp_low'
        db.add_column(u'starsystemmaker_planetmodel', 'surface_temp_low',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PlanetModel.surface_temp_high'
        db.add_column(u'starsystemmaker_planetmodel', 'surface_temp_high',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PlanetModel.surface_solidity'
        db.add_column(u'starsystemmaker_planetmodel', 'surface_solidity',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PlanetModel.ice_amount_north_pole'
        db.add_column(u'starsystemmaker_planetmodel', 'ice_amount_north_pole',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PlanetModel.ice_amount_south_pole'
        db.add_column(u'starsystemmaker_planetmodel', 'ice_amount_south_pole',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PlanetModel.ice_amount_total'
        db.add_column(u'starsystemmaker_planetmodel', 'ice_amount_total',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'PlanetModel.surface_temperature_range'
        db.add_column(u'starsystemmaker_planetmodel', 'surface_temperature_range',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'PlanetModel.ice_amount'
        db.add_column(u'starsystemmaker_planetmodel', 'ice_amount',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'PlanetModel.surface_temp_low'
        db.delete_column(u'starsystemmaker_planetmodel', 'surface_temp_low')

        # Deleting field 'PlanetModel.surface_temp_high'
        db.delete_column(u'starsystemmaker_planetmodel', 'surface_temp_high')

        # Deleting field 'PlanetModel.surface_solidity'
        db.delete_column(u'starsystemmaker_planetmodel', 'surface_solidity')

        # Deleting field 'PlanetModel.ice_amount_north_pole'
        db.delete_column(u'starsystemmaker_planetmodel', 'ice_amount_north_pole')

        # Deleting field 'PlanetModel.ice_amount_south_pole'
        db.delete_column(u'starsystemmaker_planetmodel', 'ice_amount_south_pole')

        # Deleting field 'PlanetModel.ice_amount_total'
        db.delete_column(u'starsystemmaker_planetmodel', 'ice_amount_total')


    models = {
        u'starcatalog.star': {
            'HD': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'HIP': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'HR': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['distance_parsecs']", 'object_name': 'Star'},
            'PMDec': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'PMRA': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'RA': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'RV': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'VX': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'VY': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'VZ': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'X': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'abs_mag': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'bayer_flamsteed': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'color_index': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dec': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'distance_parsecs': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'gliese': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mag': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'proper_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'spectrum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'starcatalog.starluminositytype': {
            'Meta': {'ordering': "['symbol']", 'object_name': 'StarLuminosityType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magnitude_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mass_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'radius_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'default': "'III'", 'max_length': '5'}),
            'temp_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'starcatalog.startype': {
            'Meta': {'object_name': 'StarType'},
            'age': ('django.db.models.fields.CharField', [], {'default': "'5300'", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'base_color': ('django.db.models.fields.CharField', [], {'default': "'#ffddbe'", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'radius_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surface_temp_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'default': "'K'", 'max_length': '2', 'db_index': 'True'})
        },
        u'starsystemmaker.planetfeature': {
            'Meta': {'object_name': 'PlanetFeature'},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likelihood': ('django.db.models.fields.FloatField', [], {'default': "'0.1'", 'null': 'True', 'blank': 'True'}),
            'rules_more_likely': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_required': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        u'starsystemmaker.planetmodel': {
            'Meta': {'ordering': "['name']", 'object_name': 'PlanetModel'},
            'albedo': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'atmosphere_dust_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'atmosphere_main_gas': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'atmosphere_millibars': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'atmosphere_secondary_gas': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'atmosphere_tertiary_gas': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'craterization': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gravity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ice_amount_north_pole': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ice_amount_south_pole': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ice_amount_total': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_days': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'magnetic_field': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'major_features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['starsystemmaker.PlanetFeature']", 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'mineral_surface_early': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mineral_surface_heavy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mineral_surface_late': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mineral_surface_mid': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'minerals_specific': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'oblateness': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'orbital_eccentricity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'orbital_period': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'other_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'parent_planet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['starsystemmaker.PlanetModel']", 'null': 'True', 'blank': 'True'}),
            'parent_star': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['starcatalog.Star']", 'null': 'True', 'blank': 'True'}),
            'periastron': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'periastron_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'planet_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['starsystemmaker.PlanetType']", 'null': 'True', 'blank': 'True'}),
            'plate_tectonics_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'revolution': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ring_numbers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ring_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'semi_major_axis': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solid_core_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solid_core_type': ('django.db.models.fields.CharField', [], {'default': "'Iron'", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'subsurface_ocean_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'surface_ocean_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'surface_ocean_chemicals': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'surface_solidity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'surface_temp_high': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surface_temp_low': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surface_wind_speeds_avg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'surface_wind_speeds_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tilt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'velocity_semi_amplitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'starsystemmaker.planettype': {
            'Meta': {'object_name': 'PlanetType'},
            'age_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'craterization_range': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'density_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_days_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'magnetic_field_range': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mass_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mineral_surface': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moon_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'plate_tectonics': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'radius_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'solid_core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surface_area_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'temperature_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'starsystemmaker.starmodel': {
            'Meta': {'ordering': "['star']", 'object_name': 'StarModel'},
            'base_color': ('django.db.models.fields.CharField', [], {'default': "'#ffddbe'", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'guessed_age': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_mass': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_radius': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_temp': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ids_of_companion_stars': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'json_of_closest_stars': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913', 'dim': '3', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'luminosity_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['starcatalog.StarLuminosityType']", 'null': 'True', 'blank': 'True'}),
            'luminosity_mod': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'rand_seed': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'star': ('django.db.models.fields.related.OneToOneField', [], {'default': '1', 'to': u"orm['starcatalog.Star']", 'unique': 'True'}),
            'star_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['starcatalog.StarType']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['starsystemmaker']