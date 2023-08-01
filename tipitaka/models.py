from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from mptt.models import MPTTModel, TreeForeignKey

from utils.pali_char import *

# Create your models here.

class Script(models.Model):
    code = models.CharField(max_length=20, db_index=True, verbose_name=_("Code"))
    description = models.CharField(max_length=80, blank=True, verbose_name=_("Description"))
    flag = models.ImageField(_("Flag"), upload_to="script", blank=True)

    def __str__(self):
        return f"{self.code}"
    
    def save(self, *args, **kwargs):
        val = getattr(self, 'code', False)
        if val:
            setattr(self, 'code', val.upper())
        super(Script, self).save(*args, **kwargs)



class Edition(models.Model):
    code = models.CharField(max_length=5, db_index=True, verbose_name=_("Code"))
    title = models.CharField(max_length=80, db_index=True, verbose_name=_("Title"))
    description = models.TextField(null=True, verbose_name=_("Description"))
    script = models.ForeignKey("Script", on_delete=models.SET_NULL, null=True, verbose_name=_("Script"))
    digitization = models.BooleanField(default=False, verbose_name=_("Digitization"))
    version = models.CharField(max_length=10, verbose_name=_("Version"), blank=True)

    def __str__(self):
        return f"{self.title} ({self.code})"



class Volume(models.Model):
    edition = models.ForeignKey("Edition", verbose_name=_("Edition"), on_delete=models.CASCADE)
    volume_number = models.IntegerField(db_index=True, verbose_name=_("Number"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    total_pages = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        verbose_name=_("Total pages"))
    book_cover = models.ImageField(
        upload_to = "tipitaka_book_cover", 
        null=True, blank = True,
        verbose_name = _("Book cover"))

    class Meta:
        ordering = ['volume_number']

    def __str__(self):
        return f"{_('Volume')}# {(str(self.volume_number).zfill(3))}"
    


class Page(models.Model):
    edition = models.ForeignKey("Edition", on_delete=models.CASCADE, verbose_name=_("Edition"),)
    volume = ChainedForeignKey(
        Volume,
        on_delete = models.CASCADE,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("Volume"))
    page_number = models.IntegerField(db_index=True, verbose_name=_("Page Number"))
    content = models.TextField(null=True, verbose_name=_("Content"))
    proofread = models.BooleanField(default=False, verbose_name=_("Proof-read"))
    
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
    version = models.IntegerField(default=0, verbose_name=_("Version"))
    edition = models.ForeignKey("Edition", on_delete=models.CASCADE, verbose_name=_("Edition"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Created by'))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.edition.code} v.{self.version}"

    def get_edition_and_version(self):
        return {self.pk: f"{self.edition.code} v.{self.version}"}



class WordList(models.Model):
    code = models.SlugField(default="", max_length=20, verbose_name=_("Code"))
    word = models.CharField(default="", max_length=150, verbose_name=_("Word"))
    word_seq = models.CharField(default="", verbose_name=_("Word sequence"), max_length=150)
    word_roman_script = models.CharField(default="", null=True, max_length=150, verbose_name=_("Word in roman script"))
    position = models.IntegerField(default=0, verbose_name=_("Position"))
    line_number = models.IntegerField(default=0, null=True, verbose_name=_("Line no"))
    edition = models.ForeignKey(
        "Edition",
        on_delete=models.CASCADE,
        verbose_name=_("Edition"))
    wordlist_version = ChainedForeignKey(
        WordlistVersion,
        on_delete = models.CASCADE,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("Wordlist version"))
    volume = ChainedForeignKey(
        Volume,
        on_delete = models.CASCADE,
        chained_field = "edition",
        chained_model_field = "edition",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("Volume"))
    page = ChainedForeignKey(
        Page,
        on_delete = models.CASCADE,
        chained_field = "volume",
        chained_model_field = "volume",
        show_all = False,
        auto_choose = True,
        sort = True,
        verbose_name = _("Page"))
    
    def __str__(self):
        return f"{self.code} {self.word}"
    
    # def save(self, *args, **kwargs):
    #     self.word_seq = encode(extract(clean(self.word)))
    #     self.word_roman_script = cv_pali_to_roman(extract(clean(self.word)))
    #     super().save(*args, **kwargs)

    

class TableOfContent(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True, verbose_name=_("Code"))
    wordlist_version = models.ManyToManyField(WordlistVersion,
                verbose_name=_("Wordlist version"),
                related_name="wordlist_version")
    slug = models.SlugField(default="", null=False, db_index=True, unique=True, editable=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.code



class Structure(MPTTModel):
    table_of_content = models.ForeignKey(TableOfContent, on_delete=models.CASCADE, verbose_name=_("Table of contents"),)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    code = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Code"))
    title_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Number")) 
    title = models.CharField(max_length=255, db_index=True, verbose_name=_("Title"))
    additional_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Additional Title"))
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Description") )
    ro = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Roman Script"))

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
    
    def get_descendants_include_self(self):
        return self.get_descendants(include_self=True)
    
    def get_common_reference(self):
        common_reference = CommonReference.objects.filter(structure=self).first()
        return common_reference

    def __str__(self):
        return f"{self.title}"



class CommonReference(models.Model):
    structure = models.ForeignKey("Structure", on_delete=models.CASCADE, verbose_name=_("Structure"))
    wordlist_version = models.ForeignKey("WordlistVersion", on_delete=models.CASCADE, verbose_name=_("Wordlist Version"))
    from_position = models.CharField( null=True,  max_length=20, verbose_name=_("From Position"))
    to_position = models.CharField(null=True,  max_length=20, verbose_name=_("To Position"))
    description = models.CharField(null=True,  max_length=255, verbose_name=_("Description"))

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
    

