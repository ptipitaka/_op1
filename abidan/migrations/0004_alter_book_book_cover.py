# Generated by Django 4.2 on 2023-04-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abidan', '0003_alter_book_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_cover',
            field=models.ImageField(null=True, upload_to='Abidan/Book_cover'),
        ),
    ]
