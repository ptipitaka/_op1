from django.db import models
from django.core import validators
from django.utils.text import slugify

# Create your models here.
class Book(models.Model):
    code = models.SlugField(default="", db_index=True)
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=150)
    book_cover = models.ImageField(upload_to="Abidan/Book_cover", null=True)

    def __str__(self):
        return f"{self.code} ({self.title})"

class Word(models.Model):
    word = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField()
    note = models.CharField()

    def __str__(self):
        return f"{self.word}"