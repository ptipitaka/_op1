from django.contrib import admin

# Register your models here.
from .models import Script, Edition, Volume, Page, WordListVersion, WordList

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

class WordListVersionAdmin(admin.ModelAdmin):
  list_display = ("version", "edition", "created_by",)
  list_filter = ("edition",)
  ordering = ("edition", "version",)
  
class WordListAdmin(admin.ModelAdmin):
  list_display = ("code", "word", "page",)
  ordering = ("code",)

admin.site.register(Script, ScriptAdmin)
admin.site.register(Edition, EditiontAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(WordListVersion, WordListVersionAdmin)
admin.site.register(WordList, WordListAdmin)

def get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    # Retrieve the original list
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models customably within each app.
    for app in app_list:
        if app['app_label'] == 'Tipitaka':
            ordering = {
                'Scripts': 1,
                'Editions': 2,
                'Volumes': 3,
                'Pages': 4,
                'WordListVersion': 5,
                'WordLists': 6
            }
            app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = get_app_list