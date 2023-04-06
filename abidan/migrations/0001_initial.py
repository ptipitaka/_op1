# Generated by Django 4.2 on 2023-04-06 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(default='')),
                ('title', models.CharField(max_length=50)),
                ('info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('page_number', models.PositiveIntegerField()),
                ('note', models.CharField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abidan.book')),
            ],
        ),
    ]
