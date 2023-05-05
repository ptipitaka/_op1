from django.contrib import admin

from .models import Linga
from .models import Karanta
from .models import NamaSaddamala

class LingaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "code", "title",)
    ordering = ("sequence",)

class KarantaAdmin(admin.ModelAdmin):
    list_display = ("sequence", "title",)
    ordering = ("sequence",)

class NamaSaddamalaAdmin(admin.ModelAdmin):
    list_display = ("title", "linga",)
    ordering = ("title_order",)

admin.site.register(Linga, LingaAdmin)
admin.site.register(Karanta, KarantaAdmin)
admin.site.register(NamaSaddamala, NamaSaddamalaAdmin)