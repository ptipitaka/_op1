# Generated by Django 4.2 on 2023-04-24 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipitaka', '0010_tableofcontent_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableofcontent',
            name='slug',
            field=models.SlugField(default='', editable=False, unique=True),
        ),
    ]
