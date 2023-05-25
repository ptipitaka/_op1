from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from .models import Word, WordLookup
from .tables import WordlistTable, WordlistFilter

from utils.pali_char import *


# -----------------------------------------------------
# AbidanView
# -----------------------------------------------------
class AbidanView(SingleTableMixin, FilterView):
    model = Word
    template_name = "abidan/index.html"
    context_object_name  = "wordlist"
    table_class = WordlistTable
    filterset_class = WordlistFilter

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(AbidanView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


# -----------------------------------------------------
# AbidanDetialsView
# -----------------------------------------------------
class AbidanDetialsView(DetailView):
    template_name = "abidan/details.html"
    model = Word

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AbidanDetialsView, self).get_context_data(**kwargs)
        context["word_lookup_row"] = WordLookup.objects.filter(word__exact = context["word"])
        return context
