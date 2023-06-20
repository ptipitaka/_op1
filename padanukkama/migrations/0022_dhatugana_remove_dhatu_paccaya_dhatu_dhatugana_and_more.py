# Generated by Django 4.2 on 2023-06-20 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0021_alter_dhatu_title_order_alter_paccaya_title_order'),
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
        migrations.RemoveField(
            model_name='dhatu',
            name='paccaya',
        ),
        migrations.AddField(
            model_name='dhatu',
            name='dhatugana',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='padanukkama.dhatugana', verbose_name='Dhatugana'),
        ),
        migrations.AddField(
            model_name='paccaya',
            name='dhatugana',
            field=models.ManyToManyField(to='padanukkama.dhatugana', verbose_name='Dhatugana'),
        ),
    ]
