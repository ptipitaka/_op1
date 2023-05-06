from django.urls import path

from . import views

urlpatterns = [
    path('nama-saddamala', views.NamaSaddamalaView.as_view(), name='nama_saddamala'),
    path('nama-saddamala/create/', views.NamaSaddamalaCreateView.as_view(), name='nama_saddamala_create'),
    path('nama-saddamala/<int:pk>/update/', views.NamaSaddamalaUpdateView.as_view(), name='nama_saddamala_update'),
    path('nama-saddamala/<int:pk>/delete/', views.NamaSaddamalaDeleteView.as_view(), name='nama_saddamala_delete'),
    path('akhya-saddamala', views.AkhyataSaddamalaView.as_view(), name='akhya_saddamala'),
    path('padanukkama', views.PadanukkamaView.as_view(), name='padanukkama'),
]
