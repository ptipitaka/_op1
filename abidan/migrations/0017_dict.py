# Generated by Django 4.2 on 2023-04-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abidan', '0016_alter_word_page_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dict', models.CharField()),
                ('meaning', models.TextField(null=True)),
                ('d1', models.CharField(null=True)),
                ('d2', models.CharField(null=True)),
                ('d3', models.CharField(null=True)),
            ],
        ),
    ]