from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Script(models.Model):
    code = models.CharField(max_length=20, db_index=True, verbose_name=_("code"))
    description = models.CharField(max_length=80, blank=True, verbose_name=_("description"))
    flag = models.ImageField(_("Flag"), upload_to="script", blank=True)

    def __str__(self):
        return f"{self.code}"
    
    def save(self, *args, **kwargs):
        val = getattr(self, 'code', False)
        if val:
            setattr(self, 'code', val.upper())
        super(Script, self).save(*args, **kwargs)


class Edition(models.Model):
    code = models.CharField(max_length=5, db_index=True, verbose_name=_("code"))
    title = models.CharField(max_length=80, db_index=True, verbose_name=_("title"))
    description = models.TextField(null=True, verbose_name=_("description"))
    script = models.ForeignKey("Script", verbose_name=_("script"), on_delete=models.SET_NULL, null=True)
    digitization = models.BooleanField(default=False, verbose_name=_("Digitization"))
    version = models.CharField(max_length=10, verbose_name=_("version"), blank=True)

    def __str__(self):
        return f"{self.title} ({self.code})"


class Volume(models.Model):
    edition = models.ForeignKey("Edition", verbose_name=_("edition"), on_delete=models.CASCADE)
    volume_number = models.IntegerField(db_index=True, verbose_name=_("number"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    total_pages = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        verbose_name=_("total pages"))
    book_cover = models.ImageField(
        upload_to = "tipitaka_book_cover", 
        null=True, blank = True,
        verbose_name = _("book cover"))

    def __str__(self):
        return f"{_('Volume')}# {(str(self.volume_number).zfill(3))}"
    

class Page(models.Model):
    edition = models.ForeignKey("Edition", verbose_name=_("edition"), on_delete=models.CASCADE,)
    volume = ChainedForeignKey(
        Volume,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("volume"),
        on_delete = models.CASCADE)
    page_number = models.IntegerField(db_index=True, verbose_name=_("number"))
    content = models.TextField(null=True, verbose_name=_("content"))
    proofread = models.BooleanField(verbose_name=_("Proof-read"), default=False)

    def __str__(self):
        return f"{_('Page')}# {self.page_number}"
    
    def sample_content(self):
        all_words = self.content.split(" ")
        begin_10 = all_words[:10]
        ending_3 = all_words[-3:]
        return ' '.join(begin_10 + ['....'] + ending_3)
    
    def page_ref(self):
        total_pages = self.volume.total_pages
        image_slide = {}
        image_item = 0
        url = "https://space.openpali.org/tipitaka"
        url_str = "%s/%s/%s" % (url, self.edition.code, self.volume.volume_number)
        while (image_item <= (total_pages - self.page_number)):
            image_slide[str(image_item + 1)] = "%s/%s.jpg" % (url_str, self.page_number + image_item)
            image_item += 1
            
        return image_slide


class WordlistVersion(models.Model):
    version = models.IntegerField(default=0, verbose_name=_("version"))
    edition = models.ForeignKey("Edition", verbose_name=_("edition"), on_delete=models.CASCADE,)
    created_by = models.ForeignKey(User,
                                   verbose_name=_('created_by'),
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.edition.code} {self.version}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_by = kwargs.pop('created_by')
            self.created_on = timezone.now()
        return super().save(*args, **kwargs)

class WordList(models.Model):
    code = models.CharField(default="", verbose_name=_("code"), max_length=20)
    word = models.CharField(default="", verbose_name=_("word"), max_length=150)
    word_seq = models.CharField(default="", verbose_name=_("word"), max_length=150)
    position = models.IntegerField(default=0, verbose_name=_("position"))
    line_number = models.IntegerField(default=0, verbose_name=_("line no"))
    wordlist_version = models.ForeignKey("WordlistVersion",
                                        verbose_name=_("Wordlist version"),
                                        on_delete=models.CASCADE)
    edition = models.ForeignKey("Edition", verbose_name=_("edition"), on_delete=models.CASCADE)
    volume = ChainedForeignKey(
        Volume,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("volume"),
        on_delete = models.CASCADE)
    page = ChainedForeignKey(
        Page,
        chained_field = "volume",
        chained_model_field = "volume",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("page"),
        on_delete = models.CASCADE)
    
    def __str__(self):
        return f"{self.code} {self.word}"
    

class TableOfContent(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True, verbose_name=_("code"))
    edition = models.ManyToManyField(Edition,
                limit_choices_to=Q(version__gt=0),
                verbose_name=_("edition"),
                related_name="edition")
    
    def __str__(self):
        return self.code


class Structure(MPTTModel):
    table_of_content = models.ForeignKey(TableOfContent, verbose_name=_("table of contents"), on_delete=models.CASCADE)
    code = models.CharField(max_length=20, null=True, unique=True, db_index=True, verbose_name=_("code"))
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    description = models.TextField(verbose_name=_("Description") ,max_length=255, blank=True, null=True)
    ro = models.CharField(verbose_name=_("Roman Script"), null=True, max_length=255)
    si = models.CharField(verbose_name=_("Sinhala Script"), null=True, max_length=255)
    hi = models.CharField(verbose_name=_("Hindi Script"), null=True, max_length=255)
    lo = models.CharField(verbose_name=_("Lao Script"), null=True, max_length=255)
    my = models.CharField(verbose_name=_("Myanmar Script"), null=True, max_length=255)
    km = models.CharField(verbose_name=_("Khmar Script"), null=True, max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        pass

    def get_absolute_url(self):
        return reverse('structure_detail', kwargs={'pk': self.pk, })

    def __str__(self):
        return f"{self.code} {self.title}"
    