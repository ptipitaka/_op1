from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("change-password", views.ChangePassword, name="change_password"),
    path('change-language/<str:language_code>/', views.ChangeLanguage, name='change_language'),
]