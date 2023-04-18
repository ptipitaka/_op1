from django.urls import path

from . import views

urlpatterns = [
    path('digital-archive', views.PageView.as_view(), name='digital_archive'),
    path('digital-archive/<int:pk>', views.PageDetialsUpdateView.as_view(), name='page_details'),
    path('wordlist-generator', views.WordlistGeneratorView.as_view(), name='wordlist_generator'),
]