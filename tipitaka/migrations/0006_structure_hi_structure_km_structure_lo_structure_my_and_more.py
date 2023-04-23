# Generated by Django 4.2 on 2023-04-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipitaka', '0005_alter_structure_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='hi',
            field=models.CharField(max_length=255, null=True, verbose_name='Hindi Script'),
        ),
        migrations.AddField(
            model_name='structure',
            name='km',
            field=models.CharField(max_length=255, null=True, verbose_name='Khmar Script'),
        ),
        migrations.AddField(
            model_name='structure',
            name='lo',
            field=models.CharField(max_length=255, null=True, verbose_name='Lao Script'),
        ),
        migrations.AddField(
            model_name='structure',
            name='my',
            field=models.CharField(max_length=255, null=True, verbose_name='Myanmar Script'),
        ),
        migrations.AddField(
            model_name='structure',
            name='ro',
            field=models.CharField(max_length=255, null=True, verbose_name='Roman Script'),
        ),
        migrations.AddField(
            model_name='structure',
            name='si',
            field=models.CharField(max_length=255, null=True, verbose_name='Sinhala Script'),
        ),
    ]
