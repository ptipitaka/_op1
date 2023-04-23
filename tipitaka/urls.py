from django.urls import path
from .models import Structure

from . import views

urlpatterns = [
    path('digital-archive', views.PageView.as_view(), name='digital_archive'),
    path('digital-archive/<int:pk>', views.PageDetialsUpdateView.as_view(), name='page_details'),
    path('common-toc', views.CommonTocView.as_view(), name='common_toc'),
]