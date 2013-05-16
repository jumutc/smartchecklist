# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'CheckList.last_update_time'
        db.add_column('SmartChecklist_checklist', 'last_update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'CheckList.last_update_time'
        db.delete_column('SmartChecklist_checklist', 'last_update_time')
    
    
    models = {
        'SmartChecklist.checklist': {
            'Meta': {'object_name': 'CheckList'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['SmartChecklist.DictionaryItem']", 'symmetrical': 'False'}),
            'last_update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'})
        },
        'SmartChecklist.dictionarycategory': {
            'Meta': {'object_name': 'DictionaryCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'SmartChecklist.dictionaryitem': {
            'Meta': {'object_name': 'DictionaryItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SmartChecklist.DictionaryCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '10', 'decimal_places': '5'})
        },
        'SmartChecklist.histogramitem': {
            'Meta': {'object_name': 'HistogramItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'histogramitem_a_set'", 'to': "orm['SmartChecklist.DictionaryItem']"}),
            'item_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'histogramitem_b_set'", 'to': "orm['SmartChecklist.DictionaryItem']"}),
            'probability': ('django.db.models.fields.DecimalField', [], {'default': "'1.0'", 'max_digits': '6', 'decimal_places': '5'})
        },
        'SmartChecklist.promoteditem': {
            'Meta': {'object_name': 'PromotedItem', '_ormbases': ['SmartChecklist.DictionaryItem']},
            'dictionaryitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['SmartChecklist.DictionaryItem']", 'unique': 'True', 'primary_key': 'True'}),
            'expiration_time': ('django.db.models.fields.DateTimeField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['SmartChecklist.Store']"})
        },
        'SmartChecklist.store': {
            'Meta': {'object_name': 'Store'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['SmartChecklist.Tag']", 'symmetrical': 'False'})
        },
        'SmartChecklist.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'SmartChecklist.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'checklists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['SmartChecklist.CheckList']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['SmartChecklist']
