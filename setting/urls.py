from django.urls import path

from . import views

urlpatterns = [
    # nama-saddamala
    path('nama-saddamala/', views.NamaSaddamalaView.as_view(), name='nama_saddamala'),
    path('nama-saddamala/create/', views.NamaSaddamalaCreateView.as_view(), name='nama_saddamala_create'),
    path('nama-saddamala/<int:pk>/update/', views.NamaSaddamalaUpdateView.as_view(), name='nama_saddamala_update'),
    path('nama-saddamala/<int:pk>/delete/', views.NamaSaddamalaDeleteView.as_view(), name='nama_saddamala_delete'),
    # noun-declension
    path('noun-declension/', views.NounDeclensionView.as_view(), name='noun_declension'),
    path('noun-declension/create/', views.NounDeclensionCreateView.as_view(), name='noun_declension_create'),
    path('noun-declension/<int:pk>/update/', views.NounDeclensionUpdateView.as_view(), name='noun_declension_update'),
    path('noun-declension/<int:pk>/delete/', views.NounDeclensionDeleteView.as_view(), name='noun_declension_delete'),
    # dhatu
    path('dhatu/', views.DhatuView.as_view(), name='dhatu'),
    path('dhatu/create/', views.DhatuCreateView.as_view(), name='dhatu_create'),
    path('dhatu/<int:pk>/update/', views.DhatuUpdateView.as_view(), name='dhatu_update'),
    path('dhatu/<int:pk>/delete/', views.DhatuDeleteView.as_view(), name='dhatu_delete'),
    # verb-conjugation
    path('verb-conjugation/', views.VerbConjugationView.as_view(), name='verb_conjugation'),
    path('verb-conjugation/create/', views.VerbConjugationCreateView.as_view(), name='verb_conjugation_create'),
    path('verb-conjugation/<int:pk>/update/', views.VerbConjugationUpdateView.as_view(), name='verb_conjugation_update'),
    path('verb-conjugation/<int:pk>/delete/', views.VerbConjugationDeleteView.as_view(), name='verb_conjugation_delete'),
]
