# Generated by Django 4.2 on 2023-06-01 23:08

from django.db import migrations
import django_editorjs_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0010_alter_sadda_construction_alter_sadda_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sadda',
            name='description',
            field=django_editorjs_fields.fields.EditorJsTextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
