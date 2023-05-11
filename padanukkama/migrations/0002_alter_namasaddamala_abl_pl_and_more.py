# Generated by Django 4.2 on 2023-05-05 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namasaddamala',
            name='abl_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='abl_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='acc_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Dutiyā bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='acc_sg',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Dutiyā Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='dat_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Catutthī Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='dat_sg',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Catutthī Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='gen_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Chaṭṭhī Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='gen_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Chaṭṭhī Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='instr_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Tatiyā Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='instr_sg',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Tatiyā Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='karanta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='padanukkama.karanta', verbose_name='Kāranta'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='linga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='padanukkama.linga', verbose_name='Liṅga'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='loc_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='loc_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='nom_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Paṭhamā Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='nom_sg',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Paṭhamā Ekavacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='voc_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ālapana Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='namasaddamala',
            name='voc_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ālapana Ekavacana'),
        ),
    ]