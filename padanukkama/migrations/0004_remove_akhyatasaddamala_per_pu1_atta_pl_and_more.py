# Generated by Django 4.2 on 2023-05-06 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padanukkama', '0003_dhatu_paccaya_akhyatasaddamala'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu1_atta_pl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu1_atta_sl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu1_para_pl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu1_para_sl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu2_atta_pl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu2_atta_sl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu2_para_pl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu2_para_sl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu3_atta_pl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu3_atta_sl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu3_para_pl',
        ),
        migrations.RemoveField(
            model_name='akhyatasaddamala',
            name='per_pu3_para_sl',
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AddField(
            model_name='akhyatasaddamala',
            name='par_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Parokkhā Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='ajj_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Ajjatanī Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='bha_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Bhavissanti Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='hit_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Hiyyattanī Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='kal_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Kālātipatti Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='pan_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Pañcamī Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='sat_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Sattamī Purisa 3 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu1_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 1 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu1_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 1 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu1_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 1 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu1_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 1 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu2_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 2 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu2_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 2 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu2_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 2 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu2_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 2 Parassapada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu3_atta_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 3 Attanopada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu3_atta_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 3 Attanopada Ekavacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu3_para_pl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 3 Parassapada Bahuvacana'),
        ),
        migrations.AlterField(
            model_name='akhyatasaddamala',
            name='vat_pu3_para_sl',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Vattamānā Purisa 3 Parassapada Ekavacana'),
        ),
    ]