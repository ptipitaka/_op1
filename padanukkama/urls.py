from django.urls import path

from . import views

urlpatterns = [
    # padanukkama
    path('project/', views.PadanukkamaView.as_view(), name='padanukkama'),
    path('project/create/', views.PadanukkamaCreateView.as_view(), name='padanukkama_create'),
    path('project/<int:pk>/update/', views.PadanukkamaUpdateView.as_view(), name='padanukkama_update'),
    path('project/<int:padanukkama_id>/pada/', views.PadanukkamaPadaView.as_view(), name='padanukkama_pada'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/split-sandhi/', views.PadaSplitSandhiView.as_view(), name='pada_split_sandhi'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/duplicate/', views.PadaDuplicateView.as_view(), name='pada_duplicate'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/declension/', views.PadaDeclensionView.as_view(), name='pada_declension'),
    path('project/<int:padanukkama_id>/pada/<int:pk>/delete/', views.PadaDeleteView.as_view(), name='pada_delete'),
    path('project/<int:pk>/delete/', views.PadanukkamaDeleteView.as_view(), name='padanukkama_delete'),
    path('find-abidan-closest-matches/', views.FindAbidanClosestMatchesView.as_view(), name='find_abidan_closest_matches'),
    path('find-sadda-closest-matches/', views.FindSaddaClosestMatchesView.as_view(), name='find_sadda_closest_matches'),
    path('create-vipatti/<template_id>/<sadda>/', views.CreateVipatti.as_view(), name='create_vipatti'),
    # sadda
    path('sadda/create/', views.CreateSaddaView.as_view(), name='sadda_create'),
    path('sadda/<int:pk>/details/', views.SaddaDetailView.as_view(), name='sadda_details'),
    # nama-saddamala
    path('nama-saddamala/', views.NamaSaddamalaView.as_view(), name='nama_saddamala'),
    path('nama-saddamala/create/', views.NamaSaddamalaCreateView.as_view(), name='nama_saddamala_create'),
    path('nama-saddamala/<int:pk>/update/', views.NamaSaddamalaUpdateView.as_view(), name='nama_saddamala_update'),
    path('nama-saddamala/<int:pk>/delete/', views.NamaSaddamalaDeleteView.as_view(), name='nama_saddamala_delete'),
    # akhyata-saddamala
    path('akhyata-saddamala/', views.AkhyataSaddamalaView.as_view(), name='akhyata_saddamala'),
    path('akhyata-saddamala/create/', views.AkhyataSaddamalaCreateView.as_view(), name='akhyata_saddamala_create'),
    path('akhyata-saddamala/<int:pk>/update/', views.AkhyataSaddamalaUpdateView.as_view(), name='akhyata_saddamala_update'),
    path('akhyata-saddamala/<int:pk>/delete/', views.AkhyataSaddamalaDeleteView.as_view(), name='akhyata_saddamala_delete'),
     # sadda
    # path('sadda-create/', views.CreateSaddaView.as_view(), name='sadda_create'),
    # path('sadda-detail/', views.SaddaDetailView.as_view(), name='sadda_detail'),
]
