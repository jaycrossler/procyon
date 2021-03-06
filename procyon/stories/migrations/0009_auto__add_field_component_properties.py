# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Component.properties'
        db.add_column(u'stories_component', 'properties',
                      self.gf('jsonfield.fields.JSONField')(default='{}', null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Component.properties'
        db.delete_column(u'stories_component', 'properties')


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
        u'stories.component': {
            'Meta': {'ordering': "('type', 'name')", 'object_name': 'Component', '_ormbases': [u'stories.SnippetBase']},
            'effects': ('jsonfield.fields.JSONField', [], {'default': "'[]'", 'null': 'True', 'blank': 'True'}),
            'properties': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            u'snippetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stories.SnippetBase']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Power'", 'max_length': '200', 'blank': 'True'})
        },
        u'stories.snippetbase': {
            'Meta': {'object_name': 'SnippetBase'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anthology': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Text'", 'max_length': '200', 'blank': 'True'}),
            'requirements': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'stories.story': {
            'Meta': {'ordering': "('year_min', '-created_at')", 'object_name': 'Story', '_ormbases': [u'stories.SnippetBase']},
            'choices': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'following_stories': ('jsonfield.fields.JSONField', [], {'default': '[]'}),
            'force_usage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_times_usable': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'not_if_previous_stories': ('jsonfield.fields.JSONField', [], {'default': '[]'}),
            u'snippetbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stories.SnippetBase']", 'unique': 'True', 'primary_key': 'True'}),
            'story': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'times_used': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Quest'", 'max_length': '200'}),
            'variables': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'year_max': ('django.db.models.fields.IntegerField', [], {'default': '2100'}),
            'year_min': ('django.db.models.fields.IntegerField', [], {'default': '1000'})
        },
        u'stories.storyimage': {
            'Meta': {'object_name': 'StoryImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['stories.Story']"})
        }
    }

    complete_apps = ['stories']