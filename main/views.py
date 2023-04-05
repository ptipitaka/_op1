from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _

# Create your views here.
class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_name"] = _("OPENPALI")
        return context