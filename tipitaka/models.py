from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from mptt.models import MPTTModel, TreeForeignKey

from utils.pali_char import *

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

    class Meta:
        ordering = ['volume_number']

    def __str__(self):
        return f"{_('Volume')}# {(str(self.volume_number).zfill(3))}"
    

class Page(models.Model):
    edition = models.ForeignKey("Edition", on_delete=models.CASCADE, verbose_name=_("Edition"),)
    volume = ChainedForeignKey(
        Volume,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("Volume"),
        on_delete = models.CASCADE)
    page_number = models.IntegerField(db_index=True, verbose_name=_("Page Number"))
    content = models.TextField(null=True, verbose_name=_("Content"))
    proofread = models.BooleanField(verbose_name=_("Proof-read"), default=False)
    
    class Meta:
        ordering = ['page_number']

    def __str__(self):
        return f"{_('Page')}# {self.page_number}"

    def sample_content(self):
        all_words = self.content.split(" ")
        begin_10 = all_words[:10]
        ending_3 = all_words[-3:]
        return ' '.join(begin_10 + ['....'] + ending_3)
    
    def image_ref(self):
        url = "https://space.openpali.org/tipitaka"
        url_str = "%s/%s/%s" % (url, self.edition.code, self.volume.volume_number)
        return "%s/%s.jpg" % (url_str, self.page_number)

    def page_ref(self):
        total_pages = self.volume.total_pages
        image_slide = {}
        image_item = 0
        url = "https://space.openpali.org/tipitaka"
        url_str = "%s/%s/%s" % (url, self.edition.code, self.volume.volume_number)
        while (image_item <= (total_pages - self.page_number)):
            image_slide[str(image_item + 1)] = "%s/%s.jpg" % (url_str, self.page_number + image_item)
            image_item += 1
            if image_item >= 5:
                break
            
        return image_slide


class WordlistVersion(models.Model):
    version = models.IntegerField(default=0, verbose_name=_("version"))
    edition = models.ForeignKey("Edition", on_delete=models.CASCADE, verbose_name=_("edition"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('created by'))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.edition.code} v.{self.version}"

    def get_edition_and_version(self):
        return {self.pk: f"{self.edition.code} v.{self.version}"}


class WordList(models.Model):
    code = models.SlugField(default="", max_length=20, verbose_name=_("code"))
    word = models.CharField(default="", max_length=150, verbose_name=_("word"))
    word_seq = models.CharField(default="", verbose_name=_("word sequence"), max_length=150)
    word_roman_script = models.CharField(default="", null=True, max_length=150, verbose_name=_("word in roman script"))
    position = models.IntegerField(default=0, verbose_name=_("position"))
    line_number = models.IntegerField(default=0, null=True, verbose_name=_("line no"))
    edition = models.ForeignKey(
        "Edition",
        verbose_name=_("edition"),
        on_delete=models.CASCADE)
    wordlist_version = ChainedForeignKey(
        WordlistVersion,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("wordlist version"),
        on_delete = models.CASCADE)
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
    
    def save(self, *args, **kwargs):
        self.word_seq = encode(extract(clean(self.word)))
        self.word_roman_script = cv_pali_to_roman(extract(clean(self.word)))
        super().save(*args, **kwargs)

    

class TableOfContent(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True, verbose_name=_("code"))
    wordlist_version = models.ManyToManyField(WordlistVersion,
                verbose_name=_("wordlist version"),
                related_name="wordlist_version")
    slug = models.SlugField(default="", null=False, db_index=True, unique=True, editable=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.code


class Structure(MPTTModel):
    table_of_content = models.ForeignKey(TableOfContent, verbose_name=_("table of contents"), on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    code = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("code"))
    title = models.CharField(verbose_name=_("Title"), db_index=True, max_length=255)
    description = models.TextField(verbose_name=_("Description") ,max_length=255, blank=True, null=True)
    ro = models.CharField(verbose_name=_("Roman Script"), null=True, db_index=True, max_length=255)
    si = models.CharField(verbose_name=_("Sinhala Script"), null=True, db_index=True, max_length=255)
    hi = models.CharField(verbose_name=_("Hindi Script"), null=True, db_index=True, max_length=255)
    lo = models.CharField(verbose_name=_("Lao Script"), null=True, db_index=True, max_length=255)
    my = models.CharField(verbose_name=_("Myanmar Script"), null=True, db_index=True, max_length=255)
    km = models.CharField(verbose_name=_("Khmar Script"), null=True, db_index=True, max_length=255)

    class MPTTMeta:
        pass

    def breadcrumb(self):
        ancestors = self.get_ancestors(ascending=True)
        return ' / '.join([str(ancestor) for ancestor in ancestors.reverse()][1:])

    def breadcrumb_option(self):
        ancestors = self.get_ancestors(ascending=True)
        bc = ' / '.join([str(ancestor) for ancestor in ancestors.reverse()]) 
        return bc + ' / ' + self.title  

    def get_absolute_url(self):
        return reverse('structure_detail', kwargs={'pk': self.pk, })

    def __str__(self):
        return f"{self.title}"
    
class CommonReference(models.Model):
    structure = models.ForeignKey("Structure", verbose_name=_("structure"), on_delete=models.CASCADE,)
    wordlist_version = models.ForeignKey("WordlistVersion", verbose_name=_("Wordlist Version"), on_delete=models.CASCADE)
    from_position = models.CharField(verbose_name=_("From Position"), null=True,  max_length=20)
    to_position = models.CharField(verbose_name=_("To Position"), null=True,  max_length=20)
    description = models.CharField(verbose_name=_("Description"), null=True,  max_length=255)

    def from_wordlist_position(self):
        wordlist = WordList.objects.get(
            Q(code=self.from_position) & Q(wordlist_version=self.wordlist_version))
        return wordlist
        
    def to_wordlist_position(self):
        wordlist = WordList.objects.get(
            Q(code=self.to_position) & Q(wordlist_version=self.wordlist_version))
        return wordlist
        
    def all_wordlist_in_from_position_page(self):
        wordlist = WordList.objects.filter(
            Q(code__startswith=self.from_position[:-4]) & Q(wordlist_version=self.wordlist_version))
        return wordlist

    def count_all_wordlist_in_from_position_page(self):
        wordlist = WordList.objects.filter(
            Q(code__startswith=self.from_position[:-4]) & Q(wordlist_version=self.wordlist_version))
        return len(wordlist)

    def all_wordlist_in_to_position_page(self):
        wordlist = WordList.objects.filter(
            Q(code__startswith=self.to_position[:-4]) & Q(wordlist_version=self.wordlist_version))
        return wordlist

    def count_all_wordlist_in_to_position_page(self):
        wordlist = WordList.objects.filter(
            Q(code__startswith=self.to_position[:-4]) & Q(wordlist_version=self.wordlist_version))
        return len(wordlist)
    

