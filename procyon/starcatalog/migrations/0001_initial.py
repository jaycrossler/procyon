# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StarPossiblyHabitable'
        db.create_table(u'starcatalog_starpossiblyhabitable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('HIP', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'starcatalog', ['StarPossiblyHabitable'])

        # Adding model 'StarType'
        db.create_table(u'starcatalog_startype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(default='K', max_length=2, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('surface_temp_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('base_color', self.gf('django.db.models.fields.CharField')(default='#ffddbe', max_length=8, null=True, blank=True)),
            ('mass_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('radius_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('luminosity_range', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.CharField')(default='5300', max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'starcatalog', ['StarType'])

        # Adding model 'Star'
        db.create_table(u'starcatalog_star', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('HIP', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('HD', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('HR', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('gliese', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=40, null=True, blank=True)),
            ('bayer_flamsteed', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('proper_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('RA', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dec', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('distance_parsecs', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('PMRA', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('PMDec', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('RV', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mag', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('abs_mag', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('spectrum', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('color_index', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('X', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('Y', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('Z', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('VX', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('VY', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('VZ', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'starcatalog', ['Star'])

        # Adding model 'Planet'
        db.create_table(u'starcatalog_planet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('mass', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('semi_major_axis', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_period', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbital_eccentricity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('periastron_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('velocity_semi_amplitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('other_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=60, null=True, blank=True)),
            ('HD', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('HR', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('HIP', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('gliese', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=40, null=True, blank=True)),
            ('kepler_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=40, null=True, blank=True)),
            ('radius', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('density', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gravity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'starcatalog', ['Planet'])


    def backwards(self, orm):
        # Deleting model 'StarPossiblyHabitable'
        db.delete_table(u'starcatalog_starpossiblyhabitable')

        # Deleting model 'StarType'
        db.delete_table(u'starcatalog_startype')

        # Deleting model 'Star'
        db.delete_table(u'starcatalog_star')

        # Deleting model 'Planet'
        db.delete_table(u'starcatalog_planet')


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