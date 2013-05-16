# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('SmartChecklist_tag', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=240, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('SmartChecklist', ['Tag'])

        # Adding model 'DictionaryCategory'
        db.create_table('SmartChecklist_dictionarycategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('SmartChecklist', ['DictionaryCategory'])

        # Adding model 'DictionaryItem'
        db.create_table('SmartChecklist_dictionaryitem', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SmartChecklist.DictionaryCategory'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=240, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=10, decimal_places=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('SmartChecklist', ['DictionaryItem'])

        # Adding model 'CheckList'
        db.create_table('SmartChecklist_checklist', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=240, null=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120, null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('SmartChecklist', ['CheckList'])

        # Adding M2M table for field items on 'CheckList'
        db.create_table('SmartChecklist_checklist_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('checklist', models.ForeignKey(orm['SmartChecklist.checklist'], null=False)),
            ('dictionaryitem', models.ForeignKey(orm['SmartChecklist.dictionaryitem'], null=False))
        ))
        db.create_unique('SmartChecklist_checklist_items', ['checklist_id', 'dictionaryitem_id'])

        # Adding model 'Store'
        db.create_table('SmartChecklist_store', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('SmartChecklist', ['Store'])

        # Adding M2M table for field tags on 'Store'
        db.create_table('SmartChecklist_store_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('store', models.ForeignKey(orm['SmartChecklist.store'], null=False)),
            ('tag', models.ForeignKey(orm['SmartChecklist.tag'], null=False))
        ))
        db.create_unique('SmartChecklist_store_tags', ['store_id', 'tag_id'])

        # Adding model 'PromotedItem'
        db.create_table('SmartChecklist_promoteditem', (
            ('dictionaryitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['SmartChecklist.DictionaryItem'], unique=True, primary_key=True)),
            ('expiration_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['SmartChecklist.Store'])),
        ))
        db.send_create_signal('SmartChecklist', ['PromotedItem'])

        # Adding model 'HistogramItem'
        db.create_table('SmartChecklist_histogramitem', (
            ('item_b', self.gf('django.db.models.fields.related.ForeignKey')(related_name='histogramitem_b_set', to=orm['SmartChecklist.DictionaryItem'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('probability', self.gf('django.db.models.fields.DecimalField')(default='1.0', max_digits=6, decimal_places=5)),
            ('item_a', self.gf('django.db.models.fields.related.ForeignKey')(related_name='histogramitem_a_set', to=orm['SmartChecklist.DictionaryItem'])),
        ))
        db.send_create_signal('SmartChecklist', ['HistogramItem'])

        # Adding model 'UserProfile'
        db.create_table('SmartChecklist_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('SmartChecklist', ['UserProfile'])

        # Adding M2M table for field checklists on 'UserProfile'
        db.create_table('SmartChecklist_userprofile_checklists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['SmartChecklist.userprofile'], null=False)),
            ('checklist', models.ForeignKey(orm['SmartChecklist.checklist'], null=False))
        ))
        db.create_unique('SmartChecklist_userprofile_checklists', ['userprofile_id', 'checklist_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('SmartChecklist_tag')

        # Deleting model 'DictionaryCategory'
        db.delete_table('SmartChecklist_dictionarycategory')

        # Deleting model 'DictionaryItem'
        db.delete_table('SmartChecklist_dictionaryitem')

        # Deleting model 'CheckList'
        db.delete_table('SmartChecklist_checklist')

        # Removing M2M table for field items on 'CheckList'
        db.delete_table('SmartChecklist_checklist_items')

        # Deleting model 'Store'
        db.delete_table('SmartChecklist_store')

        # Removing M2M table for field tags on 'Store'
        db.delete_table('SmartChecklist_store_tags')

        # Deleting model 'PromotedItem'
        db.delete_table('SmartChecklist_promoteditem')

        # Deleting model 'HistogramItem'
        db.delete_table('SmartChecklist_histogramitem')

        # Deleting model 'UserProfile'
        db.delete_table('SmartChecklist_userprofile')

        # Removing M2M table for field checklists on 'UserProfile'
        db.delete_table('SmartChecklist_userprofile_checklists')
    
    
    models = {
        'SmartChecklist.checklist': {
            'Meta': {'object_name': 'CheckList'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['SmartChecklist.DictionaryItem']", 'symmetrical': 'False'}),
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
