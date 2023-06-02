# Generated by Django 4.2 on 2023-06-01 14:20

from django.db import migrations, models
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0009_sadda_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sadda',
            name='construction',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Construction'),
        ),
        migrations.AlterField(
            model_name='sadda',
            name='description',
            field=django_editorjs.fields.EditorJsField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
