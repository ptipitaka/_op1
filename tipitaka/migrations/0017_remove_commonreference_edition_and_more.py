# Generated by Django 4.2 on 2023-04-29 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tipitaka', '0016_remove_tableofcontent_edition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commonreference',
            name='edition',
        ),
        migrations.AddField(
            model_name='commonreference',
            name='wordlist_version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tipitaka.wordlistversion', verbose_name='wordlist_version'),
            preserve_default=False,
        ),
    ]
