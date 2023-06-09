# Generated by Django 4.2 on 2023-05-24 16:24

import django.core.validators
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
                ('code', models.SlugField(default='', verbose_name='code')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('subtitle', models.CharField(max_length=150, verbose_name='subtitle')),
                ('book_cover', models.ImageField(null=True, upload_to='abidan_book_cover', verbose_name='book cover')),
                ('total_pages', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='total pages')),
            ],
        ),
        migrations.CreateModel(
            name='WordLookup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(null=True)),
                ('dict', models.CharField()),
                ('meaning', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='word')),
                ('burmese', models.CharField(max_length=100, null=True, verbose_name='burmese')),
                ('roman', models.CharField(max_length=100, null=True, verbose_name='roman')),
                ('word_seq', models.CharField(max_length=100, null=True, verbose_name='word sequence')),
                ('page_number', models.IntegerField(verbose_name='page no')),
                ('note', models.CharField(null=True, verbose_name='note')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abidan.book', verbose_name='book')),
            ],
        ),
    ]
