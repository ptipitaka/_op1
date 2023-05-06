from django.contrib import admin

# Register your models here.
from .models import Script, Edition, Volume, Page, WordlistVersion, WordList, TableOfContent, Structure, CommonReference
from django_mptt_admin.admin import DjangoMpttAdmin



# Register your models here.
class ScriptAdmin(admin.ModelAdmin):
  list_display = ("code", "flag", "description",)
  ordering = ("code",)

class EditiontAdmin(admin.ModelAdmin):
  list_display = ("code", "title", "script", "digitization", "version",)
  list_filter = ("digitization",)
  ordering = ("code",)

class VolumeAdmin(admin.ModelAdmin):
  list_display = ("volume_number", "name", "total_pages", "edition",)
  list_filter = ("edition",)
  ordering = ("edition", "volume_number",)

class PageAdmin(admin.ModelAdmin):
  list_display = ("edition", "volume", "page_number",)
  list_filter = ("edition", "volume",)
  ordering = ("volume", "page_number",)

class WordlistVersionAdmin(admin.ModelAdmin):
  list_display = ("version", "edition", "created_by",)
  list_filter = ("edition",)
  ordering = ("edition", "version",)
  
class WordListAdmin(admin.ModelAdmin):
  list_display = ("code", "word", "page",)
  list_filter = ("edition", "wordlist_version")
  ordering = ("code",)

class TableOfContentAdmin(admin.ModelAdmin):
   list_display = ("code",)
   list_filter = ("wordlist_version",)
   ordering = ("code",)
   prepopulated_fields = {'slug': ('code',)}

class StructureAdmin(DjangoMpttAdmin):
  def is_drag_and_drop_enabled(self):
    return True
   
class CommonReferenceAdmin(admin.ModelAdmin):
   list_display = ("structure", "wordlist_version", "from_position", "to_position",)
   list_filter = ("structure", "wordlist_version",)
   ordering = ("structure",)


admin.site.register(Script, ScriptAdmin)
admin.site.register(Edition, EditiontAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(WordlistVersion, WordlistVersionAdmin)
admin.site.register(WordList, WordListAdmin)
admin.site.register(TableOfContent, TableOfContentAdmin)
admin.site.register(Structure, StructureAdmin)
admin.site.register(CommonReference, CommonReferenceAdmin)

