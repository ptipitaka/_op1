from django.urls import path

from . import views

urlpatterns = [
    path('nama-saddhamala', views.NamaSaddamalaView.as_view(), name='nama_saddhamala'),
    path('akhya-saddhamala', views.AkhyataSaddamalaView.as_view(), name='akhya_saddhamala'),
    path('padanukkama', views.PadanukkamaView.as_view(), name='padanukkama'),
]
