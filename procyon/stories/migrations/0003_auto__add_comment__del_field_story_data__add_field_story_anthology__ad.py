# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table(u'stories_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            ('text', self.gf('django.db.models.fields.TextField')(default='', max_length=400, blank=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('importance', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stories', ['Comment'])

        # Deleting field 'Story.data'
        db.delete_column(u'stories_story', 'data')

        # Adding field 'Story.anthology'
        db.add_column(u'stories_story', 'anthology',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Story.tags'
        db.add_column(u'stories_story', 'tags',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Story.type'
        db.add_column(u'stories_story', 'type',
                      self.gf('django.db.models.fields.CharField')(default='Quest', max_length=200),
                      keep_default=False)

        # Adding field 'Story.year_min'
        db.add_column(u'stories_story', 'year_min',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'Story.year_max'
        db.add_column(u'stories_story', 'year_max',
                      self.gf('django.db.models.fields.IntegerField')(default=2100),
                      keep_default=False)

        # Adding field 'Story.times_used'
        db.add_column(u'stories_story', 'times_used',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Story.force_usage'
        db.add_column(u'stories_story', 'force_usage',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Story.requirements'
        db.add_column(u'stories_story', 'requirements',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'Story.story'
        db.add_column(u'stories_story', 'story',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'Story.options'
        db.add_column(u'stories_story', 'options',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'Story.following_stories'
        db.add_column(u'stories_story', 'following_stories',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Adding field 'Story.not_if_previous_stories'
        db.add_column(u'stories_story', 'not_if_previous_stories',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table(u'stories_comment')

        # Adding field 'Story.data'
        db.add_column(u'stories_story', 'data',
                      self.gf('jsonfield.fields.JSONField')(default={}),
                      keep_default=False)

        # Deleting field 'Story.anthology'
        db.delete_column(u'stories_story', 'anthology')

        # Deleting field 'Story.tags'
        db.delete_column(u'stories_story', 'tags')

        # Deleting field 'Story.type'
        db.delete_column(u'stories_story', 'type')

        # Deleting field 'Story.year_min'
        db.delete_column(u'stories_story', 'year_min')

        # Deleting field 'Story.year_max'
        db.delete_column(u'stories_story', 'year_max')

        # Deleting field 'Story.times_used'
        db.delete_column(u'stories_story', 'times_used')

        # Deleting field 'Story.force_usage'
        db.delete_column(u'stories_story', 'force_usage')

        # Deleting field 'Story.requirements'
        db.delete_column(u'stories_story', 'requirements')

        # Deleting field 'Story.story'
        db.delete_column(u'stories_story', 'story')

        # Deleting field 'Story.options'
        db.delete_column(u'stories_story', 'options')

        # Deleting field 'Story.following_stories'
        db.delete_column(u'stories_story', 'following_stories')

        # Deleting field 'Story.not_if_previous_stories'
        db.delete_column(u'stories_story', 'not_if_previous_stories')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stories.comment': {
            'Meta': {'ordering': "('-importance', '-created_at')", 'object_name': 'Comment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stories.Story']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '400', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'stories.story': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Story'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anthology': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'following_stories': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'force_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Story'", 'max_length': '200'}),
            'not_if_previous_stories': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'options': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'requirements': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'story': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True'}),
            'times_used': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Quest'", 'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'year_max': ('django.db.models.fields.IntegerField', [], {'default': '2100'}),
            'year_min': ('django.db.models.fields.IntegerField', [], {'default': '1000'})
        }
    }

    complete_apps = ['stories']