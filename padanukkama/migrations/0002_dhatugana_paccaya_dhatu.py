# Generated by Django 4.2 on 2023-06-20 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dhatugana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField(verbose_name='Sequence')),
                ('title', models.CharField(max_length=80, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=80, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Paccaya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Title')),
                ('title_order', models.CharField(blank=True, max_length=80, null=True, verbose_name='Title order')),
                ('dhatugana', models.ManyToManyField(to='padanukkama.dhatugana', verbose_name='Dhatugana')),
            ],
        ),
        migrations.CreateModel(
            name='Dhatu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Title')),
                ('title_order', models.CharField(blank=True, max_length=80, null=True, verbose_name='Title order')),
                ('definition', models.CharField(max_length=80, verbose_name='Definition')),
                ('meaning', models.CharField(max_length=80, verbose_name='Meaning')),
                ('popularity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Popularity')),
                ('dhatugana', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='padanukkama.dhatugana', verbose_name='Dhatugana')),
            ],
        ),
    ]
