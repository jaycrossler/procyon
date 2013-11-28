# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlanetModel'
        db.create_table(u'starcatalog_planetmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('planet_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['starcatalog.PlanetType'], null=True, blank=True)),
            ('mass', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('density', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gravity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('semi_major_axis', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_period', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_eccentricity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('velocity_semi_amplitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('other_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('star', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['starcatalog.Star'], null=True, blank=True)),
        ))
        db.send_create_signal(u'starcatalog', ['PlanetModel'])

        # Adding model 'PlanetType'
        db.create_table(u'starcatalog_planettype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('mass_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('radius_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('age_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('surface_area_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('moon_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('gravity_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('length_days_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('temperature_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('magnetic_field_range', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('craterization_range', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('mineral_surface', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('solid_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('plate_tectonics', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'starcatalog', ['PlanetType'])


    def backwards(self, orm):
        # Deleting model 'PlanetModel'
        db.delete_table(u'starcatalog_planetmodel')

        # Deleting model 'PlanetType'
        db.delete_table(u'starcatalog_planettype')


    models = {
        u'starcatalog.planet': {
            'HD': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'HIP': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'HR': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['name']", 'object_name': 'Planet'},
            'density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gliese': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'gravity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kepler_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'orbital_eccentricity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'orbital_period': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'other_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'periastron': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'periastron_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'semi_major_axis': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'velocity_semi_amplitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'starcatalog.planetmodel': {
            'Meta': {'ordering': "['name']", 'object_name': 'PlanetModel'},
            'density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gravity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'orbital_eccentricity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'orbital_period': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'other_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'periastron': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'periastron_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'planet_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['starcatalog.PlanetType']", 'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'semi_major_axis': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'star': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['starcatalog.Star']", 'null': 'True', 'blank': 'True'}),
            'velocity_semi_amplitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'starcatalog.planettype': {
            'Meta': {'object_name': 'PlanetType'},
            'age_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'craterization_range': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'gravity_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_days_range': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'magnetic_field_range': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
        u'starcatalog.starmodel': {
            'Meta': {'ordering': "['star']", 'object_name': 'StarModel'},
            'base_color': ('django.db.models.fields.CharField', [], {'default': "'#ffddbe'", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'guessed_age': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_luminosity': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_mass': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_radius': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'guessed_temp': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rand_seed': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'star': ('django.db.models.fields.related.OneToOneField', [], {'default': '1', 'to': u"orm['starcatalog.Star']", 'unique': 'True'}),
            'star_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['starcatalog.StarType']", 'null': 'True', 'blank': 'True'})
        },
        u'starcatalog.starpossiblyhabitable': {
            'HIP': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'StarPossiblyHabitable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        }
    }

    complete_apps = ['starcatalog']