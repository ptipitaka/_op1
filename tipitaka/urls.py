from django.urls import path
from .models import Structure

from . import views

urlpatterns = [
    path('digital-archive', views.DigitalArchiveView.as_view(), name='digital_archive'),
    path('digital-archive/<int:pk>', views.DigitalArchiveDetialsView.as_view(), name='digital_archive'),
    path('toc', views.TocView.as_view(), name='toc'),
    path('toc/<slug:slug>/', views.TocTreeView.as_view(), name='toc_tree'),
]