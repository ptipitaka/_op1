from django.contrib import admin

from .models import NamaType, Linga, Karanta, NamaSaddamala, \
    Language, Padanukkama, Pada, Sadda

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

class SaddaAdmin(admin.ModelAdmin):
    list_display = ("sadda",)
    ordering = ("sadda",)

class PadaAdmin(admin.ModelAdmin):
    list_display = ("pada",)
    ordering = ("pada",)


admin.site.register(NamaType, NamaTypeAdmin)
admin.site.register(Linga, LingaAdmin)
admin.site.register(Karanta, KarantaAdmin)
admin.site.register(NamaSaddamala, NamaSaddamalaAdmin)

admin.site.register(Language, LanguageAdmin)
admin.site.register(Padanukkama, PadanukkamaAdmin)
admin.site.register(Pada, PadaAdmin)
admin.site.register(Sadda, SaddaAdmin)


