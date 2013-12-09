# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    
    depends_on = (
        ("starcatalog", "0001_initial.py"),
    )
    
    def forwards(self, orm):
        # Adding model 'StarModel'
        db.create_table(u'starsystemmaker_starmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('star', self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['starcatalog.Star'], unique=True)),
            ('star_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['starcatalog.StarType'], null=True, blank=True)),
            ('base_color', self.gf('django.db.models.fields.CharField')(default='#ffddbe', max_length=8, null=True, blank=True)),
            ('rand_seed', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('guessed_temp', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('guessed_mass', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('guessed_radius', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('guessed_luminosity', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('guessed_age', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('json_of_closest_stars', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=900913, dim=3, null=True, blank=True)),
        ))
        db.send_create_signal(u'starsystemmaker', ['StarModel'])

        # Adding model 'PlanetType'
        db.create_table(u'starsystemmaker_planettype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('mass_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('radius_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('age_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('surface_area_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('moon_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('density_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('length_days_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('temperature_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('magnetic_field_range', self.gf('django.db.models.fields.CharField')(default=0, max_length=30, null=True, blank=True)),
            ('craterization_range', self.gf('django.db.models.fields.CharField')(default=0, max_length=30, null=True, blank=True)),
            ('mineral_surface', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('solid_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('plate_tectonics', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'starsystemmaker', ['PlanetType'])

        # Adding model 'PlanetFeatures'
        db.create_table(u'starsystemmaker_planetfeatures', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
        ))
        db.send_create_signal(u'starsystemmaker', ['PlanetFeatures'])

        # Adding model 'PlanetModel'
        db.create_table(u'starsystemmaker_planetmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('planet_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['starsystemmaker.PlanetType'], null=True, blank=True)),
            ('mass', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('density', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gravity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('inclination', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('oblateness', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tilt', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('albedo', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('length_days', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('surface_temperature_range', self.gf('django.db.models.fields.CharField')(default=0, max_length=30, null=True, blank=True)),
            ('magnetic_field', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('craterization', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mineral_surface_early', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mineral_surface_mid', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mineral_surface_heavy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mineral_surface_late', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('minerals_specific', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('solid_core_size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('solid_core_type', self.gf('django.db.models.fields.CharField')(default='Iron', max_length=30, null=True, blank=True)),
            ('plate_tectonics_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('surface_ocean_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('surface_ocean_chemicals', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('subsurface_ocean_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ice_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('semi_major_axis', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('revolution', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_period', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_eccentricity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('velocity_semi_amplitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ring_size', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ring_numbers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('atmosphere_millibars', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('atmosphere_main_gas', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('atmosphere_secondary_gas', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('atmosphere_tertiary_gas', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('atmosphere_dust_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('surface_wind_speeds_avg', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('surface_wind_speeds_max', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('other_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('parent_star', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['starcatalog.Star'], null=True, blank=True)),
            ('parent_planet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['starsystemmaker.PlanetModel'], null=True, blank=True)),
        ))
        db.send_create_signal(u'starsystemmaker', ['PlanetModel'])

        # Adding M2M table for field major_features on 'PlanetModel'
        m2m_table_name = db.shorten_name(u'starsystemmaker_planetmodel_major_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('planetmodel', models.ForeignKey(orm[u'starsystemmaker.planetmodel'], null=False)),
            ('planetfeatures', models.ForeignKey(orm[u'starsystemmaker.planetfeatures'], null=False))
        ))
        db.create_unique(m2m_table_name, ['planetmodel_id', 'planetfeatures_id'])


    def backwards(self, orm):
        # Deleting model 'StarModel'
        db.delete_table(u'starsystemmaker_starmodel')

        # Deleting model 'PlanetType'
        db.delete_table(u'starsystemmaker_planettype')

        # Deleting model 'PlanetFeatures'
        db.delete_table(u'starsystemmaker_planetfeatures')

        # Deleting model 'PlanetModel'
        db.delete_table(u'starsystemmaker_planetmodel')

        # Removing M2M table for field major_features on 'PlanetModel'
        db.delete_table(db.shorten_name(u'starsystemmaker_planetmodel_major_features'))


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
        u'starcatalog.startype': {
            'Meta': {'object_name': 'StarType'},
            'age': ('django.db.models.fields.CharField', [], {'default': "'5300'", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'base_color': ('django.db.models.fields.CharField', [], {'default': "'#ffddbe'", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'luminosity_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mass_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'radius_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'surface_temp_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'default': "'K'", 'max_length': '2', 'db_index': 'True'})
        },
        u'starsystemmaker.planetfeatures': {
            'Meta': {'object_name': 'PlanetFeatures'},
            'details': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'ice_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclination': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'length_days': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'magnetic_field': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'major_features': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['starsystemmaker.PlanetFeatures']", 'null': 'True', 'blank': 'True'}),
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
            'surface_temperature_range': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
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
            'guessed_luminosity': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_mass': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_radius': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_temp': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_of_closest_stars': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913', 'dim': '3', 'null': 'True', 'blank': 'True'}),
            'rand_seed': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'star': ('django.db.models.fields.related.OneToOneField', [], {'default': '1', 'to': u"orm['starcatalog.Star']", 'unique': 'True'}),
            'star_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['starcatalog.StarType']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['starsystemmaker']
