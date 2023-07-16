from django.contrib import admin

def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    app_ordering = {
        'main': 1,
        'tipitaka': 2,
        'abidan': 3,
        'padanukkama': 4
    }
    app_list.sort(key=lambda x: app_ordering.get(x['app_label'], 100))

    for app in app_list:
        if app['app_label'] == 'tipitaka':
            model_ordering = {
                'scripts': 1,
                'editions': 2,
                'volumes': 3,
                'pages': 4,
                'wordlist_version': 5,
                'wordlists': 6,
            }
            app['models'].sort(key=lambda x: model_ordering.get(x['object_name'].lower(), 100))

        if app['app_label'] == 'padanukkama':
            model_ordering = {
                'padanukkama': 1,
                'language': 2,
                'pada': 3,
                'sadda': 4,
                'namatype': 5,
                'linga': 6,
                'karanta': 7,
                'namasaddamala': 8,
                'dhatugana': 9,
                'dhatu': 10,
                'paccaya': 11,
                'akhyatasaddamala': 12,
            }
            app['models'].sort(key=lambda x: model_ordering.get(x['object_name'].lower(), 100))

    return app_list

admin.AdminSite.get_app_list = get_app_list

