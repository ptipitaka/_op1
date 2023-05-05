from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class NamaSaddamalaView(TemplateView):
    template_name = "padanukkama/nama_saddamala.html"

class AkhyataSaddamalaView(TemplateView):
    template_name = "padanukkama/akhyata_saddamala.html"

class PadanukkamaView(TemplateView):
    template_name = "padanukkama/padanukkama.html"