from django.urls import path

from . import views

urlpatterns = [
    path('nama-saddamala', views.NamaSaddamalaView.as_view(), name='nama_saddamala'),
    path('nama-saddamala/create/', views.NamaSaddamalaCreateView.as_view(), name='nama_saddamala_create'),
    path('nama-saddamala/<int:pk>/update/', views.NamaSaddamalaUpdateView.as_view(), name='nama_saddamala_update'),
    path('nama-saddamala/<int:pk>/delete/', views.NamaSaddamalaDeleteView.as_view(), name='nama_saddamala_delete'),
    path('akhyata-saddamala', views.AkhyataSaddamalaView.as_view(), name='akhyata_saddamala'),
    path('akhyata-saddamala/create/', views.AkhyataSaddamalaCreateView.as_view(), name='akhyata_saddamala_create'),
    path('akhyata-saddamala/<int:pk>/update/', views.AkhyataSaddamalaUpdateView.as_view(), name='akhyata_saddamala_update'),
    path('akhyata-saddamala/<int:pk>/delete/', views.AkhyataSaddamalaDeleteView.as_view(), name='akhyata_saddamala_delete'),
    path('padanukkama', views.PadanukkamaView.as_view(), name='padanukkama'),
    path('padanukkama/create/', views.PadanukkamaCreateView.as_view(), name='padanukkama_create'),
    path('padanukkama/<int:pk>/update/', views.PadanukkamaUpdateView.as_view(), name='padanukkama_update'),
    path('padanukkama/<int:padanukkama_id>/update/pada-sadda', views.PadanukkamaUPdatePadaSaddaView.as_view(), name='padanukkama_update_pada_sadda'),
    path('padanukkama/<int:pk>/delete/', views.PadanukkamaDeleteView.as_view(), name='padanukkama_delete'),
]
