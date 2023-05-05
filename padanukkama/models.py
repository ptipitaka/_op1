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

# class AkhyataSaddamala(models.Model):
#     pass