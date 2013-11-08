# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Planets'
        db.create_table('starcatalog_planets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('mass', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('semi_major_axis', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_period', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_eccentricity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('velocity_semi_amplitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('other_name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('HD', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('HR', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('HIPP', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('gliese', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('kepler_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('density', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gravity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('starcatalog', ['Planets'])


    def backwards(self, orm):
        # Deleting model 'Planets'
        db.delete_table('starcatalog_planets')


    models = {
        'starcatalog.planets': {
            'HD': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'HIPP': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'HR': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['name']", 'object_name': 'Planets'},
            'density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gliese': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'gravity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kepler_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'orbital_eccentricity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'orbital_period': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'other_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'periastron': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'periastron_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'radius': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'semi_major_axis': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'velocity_semi_amplitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'starcatalog.star': {
            'HD': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'HIP': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'HR': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'distance_parsecs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gliese': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mag': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'proper_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'spectrum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['starcatalog']