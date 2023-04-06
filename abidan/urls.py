from django.urls import path

from . import views

urlpatterns = [
    path('', views.AbidanView.as_view(), name='abidan'),
]