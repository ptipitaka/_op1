from django.contrib import admin

from .models import Linga, Karanta, NamaSaddamala, Dhatu, Paccaya, AkhyataSaddamala

from utils.pali_char import *

class LingaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "code", "title",)
    ordering = ("sequence",)

class KarantaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title",)
    ordering = ("sequence",)

class NamaSaddamalaAdmin(admin.ModelAdmin):    
    list_display = ("title", "linga",)
    ordering = ("title_order",)

class DhatuAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title",)
    ordering = ("sequence",)

class PaccayaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title",)
    ordering = ("sequence",)

class AkhyataSaddamalaAdmin(admin.ModelAdmin):    
    list_display = ("title", "dhatu", "paccaya",)
    ordering = ("title_order",)
    list_filter = ("dhatu", "paccaya",)

admin.site.register(Linga, LingaAdmin)
admin.site.register(Karanta, KarantaAdmin)
admin.site.register(NamaSaddamala, NamaSaddamalaAdmin)
admin.site.register(Dhatu, DhatuAdmin)
admin.site.register(Paccaya, PaccayaAdmin)
admin.site.register(AkhyataSaddamala, AkhyataSaddamalaAdmin)


