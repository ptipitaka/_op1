from django.db import models
from django.db.models import Max, Q
from django.db.models.functions import Cast
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_editorjs import EditorJsField
from django_xworkflows import models as xwf_models
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from smart_selects.db_fields import ChainedManyToManyField

from utils.pali_char import *

from tipitaka.models import WordlistVersion, TableOfContent, Structure
from .workflows import SaddaTranslationWorkflow

User = get_user_model()

# -----------------------------------------------------
# NamaType
# -----------------------------------------------------
class NamaType(models.Model):
    sequence = models.IntegerField(
        verbose_name=_("Sequence"))
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))

    def __str__(self):
        return f"{self.title}"



# -----------------------------------------------------
# Linga
# -----------------------------------------------------
class Linga(models.Model):
    sequence = models.IntegerField(
        verbose_name=_("Sequence"))
    code = models.CharField(
        max_length=5,
        verbose_name=_("Code"))
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))

    def __str__(self):
        return f"{self.code}"



# -----------------------------------------------------
# Karanta
# -----------------------------------------------------
class Karanta(models.Model):
    sequence = models.IntegerField(
        verbose_name=_("Sequence"))
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))

    def __str__(self):
        return f"{self.title}"



# -----------------------------------------------------
# NamaSaddamala
# -----------------------------------------------------
class NamaSaddamala(models.Model):
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))
    title_order = models.CharField(
        max_length=80,
        verbose_name=_("Title order"))
    title_code = models.CharField(
        max_length=80,
        verbose_name=_("Code"))
    nama_type = models.ForeignKey(
        "NamaType",
        null=True,
        blank=True,
        verbose_name=_("Type"),
        on_delete=models.SET_NULL) 
    linga = models.ForeignKey(
        "Linga",
        null=True,
        blank=True,
        verbose_name=_("Liṅga"),
        on_delete=models.SET_NULL) 
    karanta = models.ForeignKey(
        "Karanta",
        null=True,
        blank=True,
        verbose_name=_("Kāranta"),
        on_delete=models.SET_NULL) 
    nom_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Paṭhamā Ekavacana"))
    nom_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Paṭhamā Bahuvacana"))
    voc_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Ālapana Ekavacana"))
    voc_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Ālapana Bahuvacana"))
    acc_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Dutiyā Ekavacana"))
    acc_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Dutiyā Bahuvacana"))
    instr_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Tatiyā Ekavacana"))
    instr_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Tatiyā Bahuvacana"))
    dat_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Catutthī Ekavacana"))
    dat_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Catutthī Bahuvacana"))
    abl_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Pañcamī Ekavacana"))
    abl_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Pañcamī Bahuvacana"))
    gen_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Chaṭṭhī Ekavacana"))
    gen_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Chaṭṭhī Bahuvacana"))
    loc_sg = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Sattamī Ekavacana"))
    loc_pl = models.CharField(
        max_length=225,
        null=True,
        blank=True,
        verbose_name=_("Sattamī Bahuvacana"))
    popularity = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Popularity"))
    
    def __str__(self):
        return f"{self.title} ({self.linga})"

    def save(self, *args, **kwargs):
        self.title_order = encode(extract(clean(self.title)))
        super().save(*args, **kwargs)



# -----------------------------------------------------
# Language
# -----------------------------------------------------
class Language(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Language"))

    def __str__(self):
        return self.name



# -----------------------------------------------------
# Padanukkama
# -----------------------------------------------------
class Padanukkama(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"))
    about = models.TextField(
        blank=True,
        null=True, verbose_name=_("About"))
    publication = models.BooleanField(
        default=False,
        verbose_name=_("Publication"))
    collaborators = models.ManyToManyField(
        User,
        verbose_name=_("Collaborators"))
    target_languages = models.ManyToManyField(
        Language,
        verbose_name=_("Target Languages"))
    table_of_content = models.ForeignKey(
        TableOfContent,
        verbose_name=_("Table of Contents"),
        null=True,
        on_delete=models.CASCADE)
    wordlist_version = models.ManyToManyField(
        WordlistVersion,
        verbose_name=_("Wordlist Version"))
    structure = ChainedManyToManyField(
        Structure,
        chained_field="table_of_content",
        chained_model_field="table_of_content",
        verbose_name=_("Structure"),
        blank=True,
    )

    def __str__(self):
        return self.title


# -----------------------------------------------------
# Paccaya
# -----------------------------------------------------
class Paccaya(models.Model):
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))
    title_order = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name=_("Title order"))

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.title_order = encode(extract(clean(self.title)))
        super().save(*args, **kwargs)



# -----------------------------------------------------
# Dhatugana
# -----------------------------------------------------
class Dhatugana(models.Model):
    sequence = models.IntegerField(
        verbose_name=_("Sequence"))
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))
    paccaya = models.ManyToManyField(
        Paccaya,
        verbose_name=_("Paccaya"))
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"))

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.title_order = encode(extract(clean(self.title)))
        super().save(*args, **kwargs)



# -----------------------------------------------------
# Dhatu
# -----------------------------------------------------
class Dhatu(models.Model):
    title = models.CharField(
        max_length=80,
        verbose_name=_("Title"))
    title_order = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name=_("Title order"))
    dhatugana = models.ForeignKey(
        Dhatugana,
        null=True, blank=True,
        verbose_name=_("Dhatugana"),
        on_delete=models.CASCADE)
    definition = models.CharField(
        max_length=80,
        verbose_name=_("Definition"))
    meaning = models.CharField(
        max_length=80,
        verbose_name=_("Meaning"))
    popularity = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Popularity"))

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.title_order = encode(extract(clean(self.title)))
        super().save(*args, **kwargs)



# -----------------------------------------------------
# Sadda
# -----------------------------------------------------
class Sadda(xwf_models.WorkflowEnabled, models.Model):
    SADA_TYPE_CHOICES = [
        ('Nama', _('Nāma')),
        ('Akhyata', _('Akhyāta')),
        ('Byaya', _('Byaya')),
    ]
    padanukkama = models.ForeignKey(
        Padanukkama,
        on_delete=models.CASCADE,
        related_name='saddas',
        verbose_name=_("Padanukkama"))
    sadda = models.CharField(
        max_length=150,
        verbose_name=_("Sadda"))
    sadda_seq = models.CharField(
        default="",
        max_length=150,
        verbose_name=_("Pada sequence"))
    sadda_type = models.CharField(
        max_length=50,
        choices=SADA_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Type"))
    namasaddamala = models.ManyToManyField(
        NamaSaddamala,
        related_name='saddas',
        verbose_name=_("NamaSaddamala"))
    construction = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        default="",
        verbose_name=_("Construction"))
    description = EditorJsField(
        editorjs_config={
            "tools":{
                "Attaches":{"disabled":True},
                "Checklist":{"disabled":True},
                "Delimiter":{"disabled":True},
                "Embed":{"disabled":True},
                "Header":{
                    "config":{

                        "levels":[4, 5],
                        "defaultLevel":4,
                    },
                },
                "Image":{"disabled":True},
                "Link":{"disabled":True},
                "Quote":{"disabled":True},
                "Raw":{"disabled":True},
                "Warning": {"disabled":True},
            },
        },
        null=True,
        blank=True,
        verbose_name=_("Description"))
    history = HistoricalRecords()
    state = xwf_models.StateField(
                SaddaTranslationWorkflow,
                verbose_name=_("State")
            )

    def save(self, *args, **kwargs):
        self.sadda_seq = encode(extract(clean(self.sadda)))
        self.construction = '' if self.construction is None else self.construction

        super().save(*args, **kwargs)

    @classmethod
    def get_last_3_pada_updates(cls, user):
        last_3_updates = cls.history.filter(history_user=user).values('sadda')
        last_3_updates = last_3_updates.annotate(max_history_date=Max('history_date'))
        last_3_updates = last_3_updates.order_by('-max_history_date')[:3]
        
        unique_saddas = set()
        for update in last_3_updates:
            sadda_id = update['sadda']
            sadda = cls.history.get(sadda=sadda_id, history_date=update['max_history_date'])
            unique_saddas.add(sadda)
        
        return unique_saddas



# -----------------------------------------------------
# Pada
# -----------------------------------------------------
class Pada(MPTTModel):
    padanukkama = models.ForeignKey(
        Padanukkama,
        on_delete=models.CASCADE,
        related_name='pada',
        verbose_name=_("Padanukkama"))
    pada = models.CharField(
        max_length=150,
        verbose_name=_("Pada"))
    pada_seq = models.CharField(
        max_length=150,
        null=True,
        verbose_name=_("Pada sequence"))
    pada_roman_script = models.CharField(
        default="",
        null=True,
        max_length=150,
        verbose_name=_("Word in roman script"))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name='children',
        verbose_name=_("Parent word"))
    sadda = models.ForeignKey(
        "Sadda",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pada",
        verbose_name=_("Sadda"))
    
    def __str__(self):
        return f"{self.pada}"
    
    def has_descendants(self):
        return self.get_descendant_count()

    def get_current_with_descendants(self):
        descendants = self.get_descendants(include_self=True)
        return Pada.objects.filter(Q(pk=self.pk) | Q(pk__in=descendants))
    
    def get_parent_and_siblings(self):
        if self.parent:
            obj = self.parent.get_descendants(include_self=False)
            return self.parent.pada + ': ' + ' - '.join(str(sibling) for sibling in obj) 
        return ''

    def get_sandhi(self):
        if self.get_children().exists():
            children = self.get_children()
            return ' - '.join(str(child) for child in children) 
        return ''
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.pk is not None:  # Exclude the current node if it already exists in the database
            queryset = queryset.filter(pk__ne=self.pk, padanukkama=self.padanukkama)
        return queryset
    
    def get_next_record_id(self):
        next_record = Pada.objects.filter(
            id__gt=self.id, padanukkama=self.padanukkama).order_by(
            'pada_seq').first()
        if next_record:
            return next_record.id
        else:
            return None

    def get_previous_record_id(self):
        previous_record = Pada.objects.filter(
            id__lt=self.id, padanukkama=self.padanukkama).order_by(
            '-pada_seq').first()
        if previous_record:
            return previous_record.id
        else:
            return None
    
    class MPTTMeta:
        order_insertion_by = ['pada_seq']






