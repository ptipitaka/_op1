from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.
class Book(models.Model):
    code = models.SlugField(default="", db_index=True, verbose_name=_("code"))
    title = models.CharField(max_length=50, verbose_name=_("title"))
    subtitle = models.CharField(max_length=150, verbose_name=_("subtitle"))
    book_cover = models.ImageField(upload_to="abidan_book_cover", null=True, verbose_name=_("book cover"))
    total_pages = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        verbose_name=_("total pages"))
    
    def __str__(self):
        return f"{self.code} ({self.title})"

class Word(models.Model):
    word = models.CharField(max_length=100, verbose_name=_("word"))
    burmese = models.CharField(max_length=100, null=True, verbose_name=_("burmese"))
    roman = models.CharField(max_length=100, null=True, verbose_name=_("roman"))
    word_seq =models.CharField(max_length=100, null=True, verbose_name=_("word sequence"))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("book"))
    page_number = models.IntegerField(verbose_name=_("page no"))
    note = models.CharField(null=True, verbose_name=_("note"))

    def __str__(self):
        return f"{self.word}"
    
    def page_ref(self):
        total_pages = self.book.total_pages
        image_slide = {}
        image_item = 0
        url = "https://space.openpali.org/abidan"
        url_str = "%s/%s" % (url, self.book.code)
        while (image_item <= (total_pages - self.page_number)):
            image_slide[str(image_item + 1)] = "%s/%s.jpg" % (url_str, self.page_number + image_item)
            image_item += 1
            
        return image_slide
    
    
class WordLookup(models.Model):
    word = models.CharField(null=True)
    dict = models.CharField()
    meaning = models.TextField(null=True)


