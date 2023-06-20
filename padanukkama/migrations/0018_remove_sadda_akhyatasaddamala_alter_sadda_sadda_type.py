# Generated by Django 4.2 on 2023-06-19 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0017_alter_akhyatasaddamala_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sadda',
            name='akhyatasaddamala',
        ),
        migrations.AlterField(
            model_name='sadda',
            name='sadda_type',
            field=models.CharField(blank=True, choices=[('Nāma', 'NamaSaddamala'), ('Akhyāta', 'Akhyata')], max_length=50, null=True, verbose_name='Type'),
        ),
    ]