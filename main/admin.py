from django.contrib import admin

# Register your models here.
def get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    # Retrieve the original list
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the apps customably
    ordering = {
        'main': 1,
        'tipitaka': 2,
        'abidan': 3,
        'padanukkama': 4
    }
    app_list.sort(key=lambda x: ordering.get(x['app_label'], 100))
    
    # Sort the models customably within each app.
    for app in app_list:
        if app['app_label'] == 'Tipitaka':
            ordering = {
                'Scripts': 1,
                'Editions': 2,
                'Volumes': 3,
                'Pages': 4,
                'WordlistVersion': 5,
                'WordLists': 6
            }
            app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = get_app_list