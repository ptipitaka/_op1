# Generated by Django 4.2 on 2023-06-24 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_editorjs.fields
import mptt.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('padanukkama', '0007_remove_sadda_meaning_alter_sadda_sadda_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSadda',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('sadda', models.CharField(max_length=150, verbose_name='Sadda')),
                ('sadda_seq', models.CharField(default='', max_length=150, verbose_name='Pada sequence')),
                ('sadda_type', models.CharField(blank=True, choices=[('Nama', 'Nāma'), ('Akhyata', 'Akhyāta'), ('Byaya', 'Byaya')], max_length=50, null=True, verbose_name='Type')),
                ('construction', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='Construction')),
                ('description', django_editorjs.fields.EditorJsField(blank=True, null=True, verbose_name='Description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('padanukkama', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='padanukkama.padanukkama', verbose_name='Padanukkama')),
            ],
            options={
                'verbose_name': 'historical sadda',
                'verbose_name_plural': 'historical saddas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPada',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('pada', models.CharField(max_length=150, verbose_name='Pada')),
                ('pada_seq', models.CharField(max_length=150, null=True, verbose_name='Pada sequence')),
                ('pada_roman_script', models.CharField(default='', max_length=150, null=True, verbose_name='Word in roman script')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('padanukkama', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='padanukkama.padanukkama', verbose_name='Padanukkama')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='padanukkama.pada', verbose_name='Parent word')),
                ('sadda', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='padanukkama.sadda', verbose_name='Sadda')),
            ],
            options={
                'verbose_name': 'historical pada',
                'verbose_name_plural': 'historical padas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
