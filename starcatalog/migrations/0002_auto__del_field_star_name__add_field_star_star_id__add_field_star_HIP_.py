# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Star.name'
        db.delete_column('starcatalog_star', 'name')

        # Adding field 'Star.star_id'
        db.add_column('starcatalog_star', 'star_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.HIP'
        db.add_column('starcatalog_star', 'HIP',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.HD'
        db.add_column('starcatalog_star', 'HD',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.HR'
        db.add_column('starcatalog_star', 'HR',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.gliese'
        db.add_column('starcatalog_star', 'gliese',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.bayer_flamsteed'
        db.add_column('starcatalog_star', 'bayer_flamsteed',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.proper_name'
        db.add_column('starcatalog_star', 'proper_name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.RA'
        db.add_column('starcatalog_star', 'RA',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.dec'
        db.add_column('starcatalog_star', 'dec',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.distance_parsecs'
        db.add_column('starcatalog_star', 'distance_parsecs',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.PMRA'
        db.add_column('starcatalog_star', 'PMRA',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.PMDec'
        db.add_column('starcatalog_star', 'PMDec',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.RV'
        db.add_column('starcatalog_star', 'RV',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.mag'
        db.add_column('starcatalog_star', 'mag',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.abs_mag'
        db.add_column('starcatalog_star', 'abs_mag',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.spectrum'
        db.add_column('starcatalog_star', 'spectrum',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.color_index'
        db.add_column('starcatalog_star', 'color_index',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.X'
        db.add_column('starcatalog_star', 'X',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.Y'
        db.add_column('starcatalog_star', 'Y',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.Z'
        db.add_column('starcatalog_star', 'Z',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.VX'
        db.add_column('starcatalog_star', 'VX',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.VY'
        db.add_column('starcatalog_star', 'VY',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Star.VZ'
        db.add_column('starcatalog_star', 'VZ',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Star.name'
        db.add_column('starcatalog_star', 'name',
                      self.gf('django.db.models.fields.CharField')(default='star', max_length=200, unique=True),
                      keep_default=False)

        # Deleting field 'Star.star_id'
        db.delete_column('starcatalog_star', 'star_id')

        # Deleting field 'Star.HIP'
        db.delete_column('starcatalog_star', 'HIP')

        # Deleting field 'Star.HD'
        db.delete_column('starcatalog_star', 'HD')

        # Deleting field 'Star.HR'
        db.delete_column('starcatalog_star', 'HR')

        # Deleting field 'Star.gliese'
        db.delete_column('starcatalog_star', 'gliese')

        # Deleting field 'Star.bayer_flamsteed'
        db.delete_column('starcatalog_star', 'bayer_flamsteed')

        # Deleting field 'Star.proper_name'
        db.delete_column('starcatalog_star', 'proper_name')

        # Deleting field 'Star.RA'
        db.delete_column('starcatalog_star', 'RA')

        # Deleting field 'Star.dec'
        db.delete_column('starcatalog_star', 'dec')

        # Deleting field 'Star.distance_parsecs'
        db.delete_column('starcatalog_star', 'distance_parsecs')

        # Deleting field 'Star.PMRA'
        db.delete_column('starcatalog_star', 'PMRA')

        # Deleting field 'Star.PMDec'
        db.delete_column('starcatalog_star', 'PMDec')

        # Deleting field 'Star.RV'
        db.delete_column('starcatalog_star', 'RV')

        # Deleting field 'Star.mag'
        db.delete_column('starcatalog_star', 'mag')

        # Deleting field 'Star.abs_mag'
        db.delete_column('starcatalog_star', 'abs_mag')

        # Deleting field 'Star.spectrum'
        db.delete_column('starcatalog_star', 'spectrum')

        # Deleting field 'Star.color_index'
        db.delete_column('starcatalog_star', 'color_index')

        # Deleting field 'Star.X'
        db.delete_column('starcatalog_star', 'X')

        # Deleting field 'Star.Y'
        db.delete_column('starcatalog_star', 'Y')

        # Deleting field 'Star.Z'
        db.delete_column('starcatalog_star', 'Z')

        # Deleting field 'Star.VX'
        db.delete_column('starcatalog_star', 'VX')

        # Deleting field 'Star.VY'
        db.delete_column('starcatalog_star', 'VY')

        # Deleting field 'Star.VZ'
        db.delete_column('starcatalog_star', 'VZ')


    models = {
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
            'spectrum': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'star_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['starcatalog']