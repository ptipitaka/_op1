# Generated by Django 4.2 on 2023-05-30 08:15

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('padanukkama', '0005_remove_sadda_akhyatasaddamala_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sadda',
            name='akhyatasaddamala',
            field=models.ManyToManyField(to='padanukkama.akhyatasaddamala', verbose_name='Akhyatasaddamala'),
        ),
        migrations.AddField(
            model_name='sadda',
            name='namasaddamala',
            field=models.ManyToManyField(to='padanukkama.namasaddamala', verbose_name='Namasaddamala'),
        ),
        migrations.RemoveField(
            model_name='sadda',
            name='meaning',
        ),
        migrations.AddField(
            model_name='sadda',
            name='meaning',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Meaning'),
        ),
    ]
