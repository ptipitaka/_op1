from aksharamukha import transliterate
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ExportActionMixin

from .models import NamaType, Linga, Karanta, NamaSaddamala, \
    Language, Padanukkama, Pada, Sadda, Paccaya, Dhatu, Dhatugana

from utils.pali_char import *

class NamaTypeAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title",)
    ordering = ("sequence",)

class LingaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "code", "title",)
    ordering = ("sequence",)

class KarantaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title",)
    ordering = ("sequence",)

class NamaSaddamalaAdmin(admin.ModelAdmin):    
    list_display = ("popularity", "title_order", "title", "linga",)
    ordering = ("-popularity", "title_order",)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)

class PadanukkamaAdmin(admin.ModelAdmin):
    list_display = ("title",)
    ordering = ("title",)

class SaddaResource(resources.ModelResource):
    class Meta:
        model = Sadda
        fields = ('sadda_seq','sadda','sadda_type','namasaddamala','construction',)
        export_order = ('sadda_seq',)
        
    def dehydrate_namasaddamala(self, sadda):
        return ", ".join([nama.title for nama in sadda.namasaddamala.all()])

    def dehydrate_sadda(self, sadda):
        return f"{ sadda.sadda } ({transliterate.process('Thai', 'Burmese', sadda.sadda)})"

class SaddaAdmin(SimpleHistoryAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ("sadda",)
    ordering = ("sadda",)

class PadaAdmin(admin.ModelAdmin):
    list_display = ("pada",)
    ordering = ("pada",)

class PaccayaAdmin(admin.ModelAdmin):
    list_display = ("title",)
    ordering = ("title_order",)

class DhatuganaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title", "description",)
    ordering = ("sequence",)

class DhatuAdmin(admin.ModelAdmin):
    list_display = ("title", "definition", "meaning",)
    ordering = ("title_order",)



admin.site.register(NamaType, NamaTypeAdmin)
admin.site.register(Linga, LingaAdmin)
admin.site.register(Karanta, KarantaAdmin)
admin.site.register(NamaSaddamala, NamaSaddamalaAdmin)
admin.site.register(Paccaya, PaccayaAdmin)
admin.site.register(Dhatu, DhatuAdmin)
admin.site.register(Dhatugana, DhatuganaAdmin)

admin.site.register(Language, LanguageAdmin)
admin.site.register(Padanukkama, PadanukkamaAdmin)
admin.site.register(Pada, PadaAdmin)
admin.site.register(Sadda, SaddaAdmin)


