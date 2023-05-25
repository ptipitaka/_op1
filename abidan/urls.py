from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.AbidanView.as_view(), name='abidan'),
    path('<int:pk>', views.AbidanDetialsView.as_view(), name='abidan_details'),
]