from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Book(models.Model):
    code = models.SlugField(default="", db_index=True, verbose_name=_("code"))
    title = models.CharField(max_length=50, verbose_name=_("title"))
    subtitle = models.CharField(max_length=150, verbose_name=_("subtitle"))
    book_cover = models.ImageField(upload_to="abidan_book_cover", null=True, verbose_name=_("book cover"))

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
        return {
            "1": f"https://space.openpali.org/abidan/{self.book.code}/{self.page_number + 0}.jpg",
            "2": f"https://space.openpali.org/abidan/{self.book.code}/{self.page_number + 1}.jpg",
            "3": f"https://space.openpali.org/abidan/{self.book.code}/{self.page_number + 2}.jpg",
            "4": f"https://space.openpali.org/abidan/{self.book.code}/{self.page_number + 3}.jpg",
            "5": f"https://space.openpali.org/abidan/{self.book.code}/{self.page_number + 4}.jpg",
        }
    
class WordLookup(models.Model):
    word = models.CharField(null=True)
    dict = models.CharField()
    meaning = models.TextField(null=True)


