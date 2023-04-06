from django.contrib import admin

# Register your models here.
from .models import Book
from .models import Word

# Register your models here.

class BookAdmin(admin.ModelAdmin):
  list_display = ("code", "title",)

class WordAdmin(admin.ModelAdmin):
  list_display = ("word", "book", "page_number")


admin.site.register(Book, BookAdmin)
admin.site.register(Word, WordAdmin)