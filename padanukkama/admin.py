from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

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

class SaddaAdmin(SimpleHistoryAdmin):
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


