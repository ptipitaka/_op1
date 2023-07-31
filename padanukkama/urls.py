from django.urls import path

from . import views, htmx

urlpatterns = [
    # padanukkama
    path('project/', views.PadanukkamaView.as_view(), name='project'),
    path('project/create/', views.PadanukkamaCreateView.as_view(), name='padanukkama_create'),
    path('project/<int:pk>/update/', views.PadanukkamaUpdateView.as_view(), name='padanukkama_update'),
    path('project/<int:pk>/delete/', views.PadanukkamaDeleteView.as_view(), name='padanukkama_delete'),
    # pada
    path('project/<int:padanukkama_id>/pada/', views.PadanukkamaPadaView.as_view(), name='padanukkama_pada'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/split-sandhi/', views.PadaSplitSandhiView.as_view(), name='pada_split_sandhi'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/duplicate/', views.PadaDuplicateView.as_view(), name='pada_duplicate'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/declension/', views.PadaDeclensionView.as_view(), name='pada_declension'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/delete/', views.PadaDeleteView.as_view(), name='pada_delete'),
    path('add-sadda-to-padda/<int:padanukkama_id>/<int:pada_id>/<int:sadda_id>/', views.AddSaddaToPada.as_view(), name='add_sadda_to_pada'),
    path('decoupling-pada-with-sadda/<int:pada_id>/', views.DecouplingPadaWithSadda.as_view(), name='decoupling_pada_with_sadda'),
    path('find-abidan-closest-matches/', views.FindAbidanClosestMatchesView.as_view(), name='find_abidan_closest_matches'),
    path('find-sadda-closest-matches/', views.FindSaddaClosestMatchesView.as_view(), name='find_sadda_closest_matches'),
    path('find-existing-sadda/<padanukkama_id>/<sadda>/', views.FindExistingSadda.as_view(), name= 'find_existing_sadda'),
    path('create-vipatti/<padanukkama_id>/<sadda>/<sadda_type>/<template_ids>/', views.CreateVipatti.as_view(), name='create_vipatti'),
    path('filter-verb-conjugation/<str:word>/', views.FilterVerbConjugation, name='filter_verb_conjugation'),
    # sadda
    path('sadda/', views.SaddaView.as_view(), name='sadda'),
    path('sadda/<int:pk>/update/', views.SaddaUpdateView.as_view(), name='sadda_update'),
    path('find-related-padas/', views.FindRelatedPadaView.as_view(), name='find_related_pada'),
    # literal_translation
    path('literal-translation/', views.LiteralTranslationView.as_view(), name='literal_translation'),
    path('literal-translation/project/<int:padanukkama_id>/create/', views.LiteralTranslationCreateView.as_view(), name='literal_translation_create'),
    path('literal-translation/<int:pk>/update/', views.LiteralTranslationUpdateView.as_view(), name='literal_translation_update'),
    path('literal-translation/<int:pk>/delete/', views.LiteralTranslationDeleteView.as_view(), name='literal_translation_delete'),
    path('literal-translation/<int:pk>/translate/', views.LiteralTranslationTranslateView.as_view(), name='literal_translation_translate'),
]


htmx_urlpatterns = [
    # literal_translation
    path('htmx-pada-details/<int:padanukkama_id>/<pada>/', htmx.PadaDetailsView.as_view(), name='htmx_pada_details'),
]

urlpatterns += htmx_urlpatterns