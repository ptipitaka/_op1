# Generated by Django 4.2 on 2023-04-06 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abidan', '0010_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.AddField(
            model_name='book',
            name='original_id',
            field=models.IntegerField(null=True),
        ),
    ]