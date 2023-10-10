from django.contrib import messages
from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import resolve, reverse_lazy
from django.utils.translation import gettext_lazy as _

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from urllib.parse import urlencode

from padanukkama.models import NamaSaddamala, Dhatu, Linga, \
                    AkhyataSaddamala, VerbConjugation, NounDeclension
from .tables import NamaSaddamalaTable, NamaSaddamalaFilter, \
                    DhatuTable, DhatuFilter, \
                    NounDeclensionTable, NounDeclensionFilter, \
                    VerbConjugationTable, VerbConjugationFilter
from .forms import  NamaSaddamalaForm, DhatuForm, AkhyataSaddamalaForm, \
                    VerbConjugationForm, NounDeclensionForm

# ====================================================
# NamaSaddamala
# ====================================================

# NamaSaddamalaView
#------------------
class NamaSaddamalaView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = NamaSaddamala
    template_name = "setting/nama_saddamala.html"
    context_object_name  = "nama_saddamala"
    table_class = NamaSaddamalaTable
    filterset_class = NamaSaddamalaFilter
    
    def get_context_data(self, **kwargs):
        context = super(NamaSaddamalaView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context



# NamaSaddamalaCreateView
# -----------------------
class NamaSaddamalaCreateView(LoginRequiredMixin, CreateView):
    model = NamaSaddamala
    template_name = "setting/nama_saddamala_detail.html"
    form_class = NamaSaddamalaForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('nama_saddamala')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# NamaSaddamalaUpdateView
# -----------------------
class NamaSaddamalaUpdateView(LoginRequiredMixin, UpdateView):
    model = NamaSaddamala
    template_name = "setting/nama_saddamala_detail.html"
    form_class = NamaSaddamalaForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('nama_saddamala')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# NamaSaddamalaDeleteView
# -----------------------
class NamaSaddamalaDeleteView(LoginRequiredMixin, DeleteView):
    model = NamaSaddamala
    template_name = "setting/nama_saddamala_detail.html"
    success_url = reverse_lazy('nama_saddamala')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nama_saddamala'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# NamaSaddamalaListView
# ---------------------
class NamaSaddamalaListView(ListView):
    model = NamaSaddamala
    template_name = 'setting/nama_saddamala_list.html'
    context_object_name = 'lingas'

    def get_queryset(self):
        queryset = NamaSaddamala.objects.all().order_by('title')
        return Linga.objects.annotate(
            num_namasaddamala=Count('namasaddamala')).prefetch_related(
                Prefetch('namasaddamala_set', queryset=queryset))
    


# ====================================================
# Dhatu
# ====================================================

# DhatuView
# ---------
class DhatuView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Dhatu
    template_name = "setting/dhatu.html"
    context_object_name  = "dhatu"
    table_class = DhatuTable
    filterset_class = DhatuFilter
    
    def get_context_data(self, **kwargs):
        context = super(DhatuView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context



# DhatuCreateView
# ---------------
class DhatuCreateView(LoginRequiredMixin, CreateView):
    model = Dhatu
    template_name = "setting/dhatu_detail.html"
    form_class = DhatuForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('dhatu')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# DhatuUpdateView
# ---------------
class DhatuUpdateView(LoginRequiredMixin, UpdateView):
    model = Dhatu
    template_name = "setting/dhatu_detail.html"
    form_class = DhatuForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('dhatu')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# DhatuDeleteView
# ---------------
class DhatuDeleteView(LoginRequiredMixin, DeleteView):
    model = Dhatu
    template_name = "setting/dhatu_detail.html"
    success_url = reverse_lazy('dhatu')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dhatu'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context



# ====================================================
# NounDeclension
# ====================================================

# NounDeclensionView
# ---------
class NounDeclensionView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = NounDeclension
    template_name = "setting/noun_declension.html"
    context_object_name  = "noun_declension"
    table_class = NounDeclensionTable
    filterset_class = NounDeclensionFilter
    
    def get_context_data(self, **kwargs):
        context = super(NounDeclensionView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context



# NounDeclensionCreateView
# ---------------
class NounDeclensionCreateView(LoginRequiredMixin, CreateView):
    model = NounDeclension
    template_name = "setting/noun_declension_detail.html"
    form_class = NounDeclensionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('noun_declension')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# NounDeclensionUpdateView
# ---------------
class NounDeclensionUpdateView(LoginRequiredMixin, UpdateView):
    model = NounDeclension
    template_name = "setting/noun_declension_detail.html"
    form_class = NounDeclensionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('noun_declension')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# NounDeclensionDeleteView
# ---------------
class NounDeclensionDeleteView(LoginRequiredMixin, DeleteView):
    model = NounDeclension
    template_name = "setting/noun_declension_detail.html"
    success_url = reverse_lazy('noun_declension')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noun_declension'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context




# ====================================================
# Akhya
# ====================================================

# VerbConjugation
# ---------------
class VerbConjugationView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = VerbConjugation
    template_name = "setting/verb_conjugation.html"
    context_object_name  = "verb_conjugation"
    table_class = VerbConjugationTable
    filterset_class = VerbConjugationFilter
    
    def get_context_data(self, **kwargs):
        context = super(VerbConjugationView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context



# VerbConjugationCreateView
# -------------------------
class VerbConjugationCreateView(LoginRequiredMixin, CreateView):
    model = VerbConjugation
    template_name = "setting/verb_conjugation_detail.html"
    form_class = VerbConjugationForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('verb_conjugation')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# VerbConjugationUpdateView
# -------------------------
class VerbConjugationUpdateView(LoginRequiredMixin, UpdateView):
    model = VerbConjugation
    template_name = "setting/verb_conjugation_detail.html"
    form_class = VerbConjugationForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        
        # Print the detailed form errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field '{field}': {error}")
        return response

    def get_success_url(self):
        success_url = reverse_lazy('verb_conjugation')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url



# VerbConjugationDeleteView
# -------------------------
class VerbConjugationDeleteView(LoginRequiredMixin, DeleteView):
    model = VerbConjugation
    template_name = "setting/verb_conjugation_detail.html"
    success_url = reverse_lazy('verb_conjugation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verb_conjugation'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context



# AkhyataSaddamalaUpdateView
# --------------------------
class AkhyataSaddamalaUpdateOrCreateView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            obj = AkhyataSaddamala.objects.first() # Check if object exists
        except AkhyataSaddamala.DoesNotExist:
            obj = None
        
        form = AkhyataSaddamalaForm(instance=obj)
        context = {
            'form': form,
        }
        return render(request, 'setting/akhyala_saddamala.html', context)

    def post(self, request):
        try:
            obj = AkhyataSaddamala.objects.first()  # Check if object exists
        except AkhyataSaddamala.DoesNotExist:
            obj = None
        
        form = AkhyataSaddamalaForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()  # Save the object (create new or update existing)
            return redirect('akhyata_saddamala')
        
        context = {
            'form': form,
        }
        return render(request, 'setting/akhyala_saddamala.html', context)


