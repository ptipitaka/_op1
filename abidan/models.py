from django.db import models
from django.core import validators
from django.utils.text import slugify

# Create your models here.
class Book(models.Model):
    code = models.SlugField(default="", db_index=True)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=150)
    book_cover = models.ImageField(upload_to="abidan_book_cover", null=True)
    original_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.code} ({self.title})"

class Word(models.Model):
    word = models.CharField(max_length=100)
    burmese = models.CharField(max_length=100, null=True)
    roman = models.CharField(max_length=100, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.CharField(max_length=50)
    note = models.CharField(null=True)

    def __str__(self):
        return f"{self.word}"