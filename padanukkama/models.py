from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.pali_char import *

# Create your models here.
class Linga(models.Model):
    sequence = models.IntegerField(verbose_name=_("sequence"))
    code = models.CharField(max_length=5, verbose_name=_("code"))
    title = models.CharField(max_length=80, verbose_name=_("title"))

    def __str__(self):
        return f"{self.title}"

class Karanta(models.Model):
    sequence = models.IntegerField(verbose_name=_("sequence"))
    title = models.CharField(max_length=80, verbose_name=_("title"))

    def __str__(self):
        return f"{self.title}"

class NamaSaddamala(models.Model):
    title = models.CharField(max_length=80, verbose_name=_("title"))
    title_order = models.CharField(max_length=80, verbose_name=_("title order"))
    linga = models.ForeignKey("Linga", null=True, blank=True, verbose_name=_("Liṅga"), on_delete=models.SET_NULL) 
    karanta = models.ForeignKey("Karanta", null=True, blank=True, verbose_name=_("Kāranta"), on_delete=models.SET_NULL) 
    nom_sg = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Paṭhamā Ekavacana"))
    nom_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Paṭhamā Bahuvacana"))
    voc_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ālapana Ekavacana"))
    voc_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ālapana Bahuvacana"))
    acc_sg = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Dutiyā Ekavacana"))
    acc_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Dutiyā bahuvacana"))
    instr_sg = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Tatiyā Ekavacana"))
    instr_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Tatiyā Bahuvacana"))
    dat_sg = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Catutthī Ekavacana"))
    dat_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Catutthī Bahuvacana"))
    abl_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Ekavacana"))
    abl_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Bahuvacana"))
    gen_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Chaṭṭhī Ekavacana"))
    gen_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Chaṭṭhī Bahuvacana"))
    loc_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Ekavacana"))
    loc_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Bahuvacana"))
    
    def __str__(self):
        return f"{self.title} ({self.linga})"

    def save(self, *args, **kwargs):
        self.title_order = encode(extract(clean(self.title)))
        super().save(*args, **kwargs)


class Dhatu(models.Model):
    sequence = models.IntegerField(verbose_name=_("sequence"))
    title = models.CharField(max_length=80, verbose_name=_("title"))

    def __str__(self):
        return f"{self.title}"


class Paccaya(models.Model):
    sequence = models.IntegerField(verbose_name=_("sequence"))
    title = models.CharField(max_length=80, verbose_name=_("title"))

    def __str__(self):
        return f"{self.title}"

class AkhyataSaddamala(models.Model):
    title = models.CharField(max_length=80, verbose_name=_("title"))
    title_order = models.CharField(max_length=80, verbose_name=_("title order"))
    dhatu = models.ForeignKey("Dhatu", null=True, blank=True, verbose_name=_("Dhātu"), on_delete=models.SET_NULL) 
    paccaya = models.ForeignKey("Paccaya", null=True, blank=True, verbose_name=_("Paccaya"), on_delete=models.SET_NULL)
    # 1 Vattamānā (Present Tense)
    vat_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 3 Parassapada Ekavacana"))
    vat_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 3 Parassapada Bahuvacana"))
    vat_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 3 Attanopada Ekavacana"))
    vat_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 3 Attanopada Bahuvacana"))
    vat_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 2 Parassapada Ekavacana"))
    vat_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 2 Parassapada Bahuvacana"))
    vat_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 2 Attanopada Ekavacana"))
    vat_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 2 Attanopada Bahuvacana"))
    vat_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 1 Parassapada Ekavacana"))
    vat_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 1 Parassapada Bahuvacana"))
    vat_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 1 Attanopada Ekavacana"))
    vat_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Vattamānā Purisa 1 Attanopada Bahuvacana"))
    # 2 Pañcamī (Imperative Mood)
    pan_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 3 Parassapada Ekavacana"))
    pan_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 3 Parassapada Bahuvacana"))
    pan_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 3 Attanopada Ekavacana"))
    pan_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 3 Attanopada Bahuvacana"))
    pan_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 2 Parassapada Ekavacana"))
    pan_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 2 Parassapada Bahuvacana"))
    pan_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 2 Attanopada Ekavacana"))
    pan_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 2 Attanopada Bahuvacana"))
    pan_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 1 Parassapada Ekavacana"))
    pan_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 1 Parassapada Bahuvacana"))
    pan_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 1 Attanopada Ekavacana"))
    pan_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Pañcamī Purisa 1 Attanopada Bahuvacana"))
    # 3 Sattamī (Optative Mood)
    sat_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 3 Parassapada Ekavacana"))
    sat_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 3 Parassapada Bahuvacana"))
    sat_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 3 Attanopada Ekavacana"))
    sat_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 3 Attanopada Bahuvacana"))
    sat_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 2 Parassapada Ekavacana"))
    sat_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 2 Parassapada Bahuvacana"))
    sat_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 2 Attanopada Ekavacana"))
    sat_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 2 Attanopada Bahuvacana"))
    sat_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 1 Parassapada Ekavacana"))
    sat_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 1 Parassapada Bahuvacana"))
    sat_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 1 Attanopada Ekavacana"))
    sat_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Sattamī Purisa 1 Attanopada Bahuvacana"))
    # 4 Parokkhā (Perfect Tense)
    par_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 3 Parassapada Ekavacana"))
    par_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 3 Parassapada Bahuvacana"))
    par_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 3 Attanopada Ekavacana"))
    par_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 3 Attanopada Bahuvacana"))
    par_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 2 Parassapada Ekavacana"))
    par_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 2 Parassapada Bahuvacana"))
    par_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 2 Attanopada Ekavacana"))
    par_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 2 Attanopada Bahuvacana"))
    par_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 1 Parassapada Ekavacana"))
    par_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 1 Parassapada Bahuvacana"))
    par_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 1 Attanopada Ekavacana"))
    par_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Parokkhā Purisa 1 Attanopada Bahuvacana"))
    # 5 Hiyyattanī (Imperfect Tense)
    hit_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 3 Parassapada Ekavacana"))
    hit_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 3 Parassapada Bahuvacana"))
    hit_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 3 Attanopada Ekavacana"))
    hit_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 3 Attanopada Bahuvacana"))
    hit_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 2 Parassapada Ekavacana"))
    hit_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 2 Parassapada Bahuvacana"))
    hit_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 2 Attanopada Ekavacana"))
    hit_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 2 Attanopada Bahuvacana"))
    hit_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 1 Parassapada Ekavacana"))
    hit_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 1 Parassapada Bahuvacana"))
    hit_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 1 Attanopada Ekavacana"))
    hit_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Hiyyattanī Purisa 1 Attanopada Bahuvacana"))
    # 6 Ajjatanī (Aorist Tense)
    ajj_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 3 Parassapada Ekavacana"))
    ajj_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 3 Parassapada Bahuvacana"))
    ajj_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 3 Attanopada Ekavacana"))
    ajj_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 3 Attanopada Bahuvacana"))
    ajj_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 2 Parassapada Ekavacana"))
    ajj_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 2 Parassapada Bahuvacana"))
    ajj_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 2 Attanopada Ekavacana"))
    ajj_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 2 Attanopada Bahuvacana"))
    ajj_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 1 Parassapada Ekavacana"))
    ajj_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 1 Parassapada Bahuvacana"))
    ajj_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 1 Attanopada Ekavacana"))
    ajj_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Ajjatanī Purisa 1 Attanopada Bahuvacana"))
    # 7 Bhavissanti (Future Tense)
    bha_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 3 Parassapada Ekavacana"))
    bha_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 3 Parassapada Bahuvacana"))
    bha_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 3 Attanopada Ekavacana"))
    bha_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 3 Attanopada Bahuvacana"))
    bha_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 2 Parassapada Ekavacana"))
    bha_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 2 Parassapada Bahuvacana"))
    bha_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 2 Attanopada Ekavacana"))
    bha_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 2 Attanopada Bahuvacana"))
    bha_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 1 Parassapada Ekavacana"))
    bha_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 1 Parassapada Bahuvacana"))
    bha_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 1 Attanopada Ekavacana"))
    bha_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Bhavissanti Purisa 1 Attanopada Bahuvacana"))
    # 8 Kālātipatti (Conditional Mood)
    kal_pu3_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 3 Parassapada Ekavacana"))
    kal_pu3_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 3 Parassapada Bahuvacana"))
    kal_pu3_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 3 Attanopada Ekavacana"))
    kal_pu3_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 3 Attanopada Bahuvacana"))
    kal_pu2_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 2 Parassapada Ekavacana"))
    kal_pu2_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 2 Parassapada Bahuvacana"))
    kal_pu2_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 2 Attanopada Ekavacana"))
    kal_pu2_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 2 Attanopada Bahuvacana"))
    kal_pu1_para_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 1 Parassapada Ekavacana"))
    kal_pu1_para_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 1 Parassapada Bahuvacana"))
    kal_pu1_atta_sl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 1 Attanopada Ekavacana"))
    kal_pu1_atta_pl = models.CharField(max_length=225, null=True, blank=True, verbose_name=_("Kālātipatti Purisa 1 Attanopada Bahuvacana"))

    def __str__(self):
        return f"{self.title} {self.dhatu}-{self.paccaya}"

    def save(self, *args, **kwargs):
        self.title_order = encode(extract(clean(self.title)))
        super().save(*args, **kwargs)