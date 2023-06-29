# Generated by Django 4.2 on 2023-06-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0006_remove_paccaya_dhatugana_dhatugana_paccaya'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sadda',
            name='meaning',
        ),
        migrations.AlterField(
            model_name='sadda',
            name='sadda_type',
            field=models.CharField(blank=True, choices=[('Nama', 'Nāma'), ('Akhyata', 'Akhyāta'), ('Byaya', 'Byaya')], max_length=50, null=True, verbose_name='Type'),
        ),
    ]