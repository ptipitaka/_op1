from django.contrib import admin

from .models import Book
from .models import Word

class BookAdmin(admin.ModelAdmin):
  list_display = ("code", "title", "total_pages")
  ordering = ("code",)

class WordAdmin(admin.ModelAdmin):
  list_display = ("word", "book", "page_number",)
  ordering = ("word", "book", "page_number")


admin.site.register(Book, BookAdmin)
admin.site.register(Word, WordAdmin)