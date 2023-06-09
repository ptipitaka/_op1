from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

from .models import Word, WordLookup
from .tables import WordlistTable, WordlistFilter

from utils.pali_char import *


# -----------------------------------------------------
# AbidanView
# -----------------------------------------------------
class AbidanView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Word
    template_name = "abidan/index.html"
    context_object_name  = "wordlist"
    table_class = WordlistTable
    filterset_class = WordlistFilter
    
    def get_context_data(self, **kwargs):
        context = super(AbidanView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


# -----------------------------------------------------
# AbidanDetialsView
# -----------------------------------------------------
class AbidanDetialsView(LoginRequiredMixin, DetailView):
    template_name = "abidan/details.html"
    model = Word

    def get_context_data(self, **kwargs):
        context = super(AbidanDetialsView, self).get_context_data(**kwargs)
        context["word_lookup_row"] = WordLookup.objects.filter(word__exact = context["word"])
        return context
