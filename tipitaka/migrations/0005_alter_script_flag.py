# Generated by Django 4.2 on 2023-04-11 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipitaka', '0004_alter_script_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='flag',
            field=models.ImageField(blank=True, upload_to='script', verbose_name='Flag'),
        ),
    ]
