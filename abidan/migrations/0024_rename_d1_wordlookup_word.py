# Generated by Django 4.2 on 2023-04-07 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abidan', '0023_delete_dict'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wordlookup',
            old_name='d1',
            new_name='word',
        ),
    ]