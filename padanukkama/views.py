from braces import views
import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import resolve, reverse_lazy

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from mptt.exceptions import InvalidMove

from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama, Pada, Sadda

from .tables import NamaSaddamalaTable, \
                    NamaSaddamalaFilter, AkhyataSaddamalaTable, \
                    AkhyataSaddamalaFilter, PadanukkamaTable, \
                    PadanukkamaFilter, PadaTable, PadaFilter, \
                    PadaParentChildTable
from .forms import  NamaSaddamalaForm, AkhyataSaddamalaForm, \
                    PadanukkamaCreateForm, PadanukkamaUpdateForm, \
                    AddChildPadaForm, \
                    SaddaForm

from utils.pali_char import *

# -----------------------------------------------------
# NamaSaddamalaView
# -----------------------------------------------------
class NamaSaddamalaView(SingleTableMixin, FilterView):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala.html"
    context_object_name  = "nama_saddamala"
    table_class = NamaSaddamalaTable
    filterset_class = NamaSaddamalaFilter

    def get_context_data(self, **kwargs):
        context = super(NamaSaddamalaView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


# -----------------------------------------------------
# NamaSaddamalaCreateView
# -----------------------------------------------------
class NamaSaddamalaCreateView(CreateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala_detail.html"
    form_class = NamaSaddamalaForm
    success_url = reverse_lazy('nama_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# -----------------------------------------------------
# NamaSaddamalaUpdateView
# -----------------------------------------------------
class NamaSaddamalaUpdateView(UpdateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala_detail.html"
    form_class = NamaSaddamalaForm
    success_url = reverse_lazy('nama_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# -----------------------------------------------------
# NamaSaddamalaDeleteView
# -----------------------------------------------------
class NamaSaddamalaDeleteView(DeleteView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala_detail.html"
    success_url = reverse_lazy('nama_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nama_saddamala'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# -----------------------------------------------------
# AkhyataSaddamalaView
# -----------------------------------------------------
class AkhyataSaddamalaView(SingleTableMixin, FilterView):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala.html"
    context_object_name  = "akhyata_saddamala"
    table_class = AkhyataSaddamalaTable
    filterset_class = AkhyataSaddamalaFilter

    def get_context_data(self, **kwargs):
        context = super(AkhyataSaddamalaView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


# -----------------------------------------------------
# AkhyataSaddamalaCreateView
# -----------------------------------------------------
class AkhyataSaddamalaCreateView(CreateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala_detail.html"
    form_class = AkhyataSaddamalaForm
    success_url = reverse_lazy('akhyata_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# -----------------------------------------------------
# AkhyataSaddamalaUpdateView
# -----------------------------------------------------
class AkhyataSaddamalaUpdateView(UpdateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala_detail.html"
    form_class = AkhyataSaddamalaForm
    success_url = reverse_lazy('akhyata_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# -----------------------------------------------------
# AkhyataSaddamalaDeleteView
# -----------------------------------------------------
class AkhyataSaddamalaDeleteView(DeleteView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala_detail.html"
    success_url = reverse_lazy('akhyata_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['akhyata_saddamala'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


# -----------------------------------------------------
# PadanukkamaView
# -----------------------------------------------------
class PadanukkamaView(SingleTableMixin, FilterView):
    model = Padanukkama
    template_name = "padanukkama/padanukkama.html"
    context_object_name  = "padanukkama"
    table_class =PadanukkamaTable
    filterset_class =PadanukkamaFilter

    def get_context_data(self, **kwargs):
        context = super(PadanukkamaView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


# -----------------------------------------------------
# PadanukkamaCreateView
# -----------------------------------------------------
class PadanukkamaCreateView(CreateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = Padanukkama
    template_name = "padanukkama/padanukkama_create.html"
    form_class = PadanukkamaCreateForm

    def get_success_url(self):
        return reverse_lazy('padanukkama_update', args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# -----------------------------------------------------
# PadanukkamaUpdateView
# -----------------------------------------------------
class PadanukkamaUpdateView(UpdateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = Padanukkama
    context_object_name = 'padanukkama'
    template_name = "padanukkama/padanukkama_update.html"
    form_class = PadanukkamaUpdateForm
    success_url = reverse_lazy('padanukkama')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['table_of_content'] = self.object.table_of_content
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, "Form is invalid. Please correct the errors.")
        return super().form_invalid(form)


# -----------------------------------------------------
# PadanukkamaDeleteView
# -----------------------------------------------------
class PadanukkamaDeleteView(DeleteView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = Padanukkama
    success_url = reverse_lazy('padanukkama')
    template_name = "padanukkama/padanukkama_delete.html"


# -----------------------------------------------------
# PadanukkamaPadaView
# -----------------------------------------------------
class PadanukkamaPadaView(SingleTableMixin, FilterView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = Pada
    template_name = "padanukkama/pada.html"
    context_object_name = 'pada'
    table_class = PadaTable
    filterset_class = PadaFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        padanukkama_id = self.kwargs.get('padanukkama_id')
        padanukkama = get_object_or_404(Padanukkama, pk=padanukkama_id)
        queryset = Pada.objects.filter(padanukkama=padanukkama)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PadanukkamaPadaView, self).get_context_data(**kwargs)
        padanukkama_id = self.kwargs['padanukkama_id']
        context["padanukkama_id"] = padanukkama_id
        context['deleted_conf_message'] = _('Are you sure you want to delete this record?')
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


# -----------------------------------------------------
# PadaSplitSandhiView
# -----------------------------------------------------
class PadaSplitSandhiView(View, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    template_name = 'padanukkama/pada_split_sandhi.html'

    def get(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, id=pk)
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        form = AddChildPadaForm()
        table = PadaParentChildTable(data=pada.get_current_with_descendants())
        message = _('Are you sure you want to delete this record?')

        return render(request, self.template_name, {'form': form, 'pada': pada, 'table':table, 'message':message})
    
    def post(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, id=pk)
        form = AddChildPadaForm(request.POST)
        if form.is_valid():
            child_pada = form.save(commit=False)
            child_pada.parent = pada
            child_pada.padanukkama = pada.padanukkama
            child_pada.pada_seq = encode(extract(clean(pada.pada)))
            child_pada.pada_roman_script = cv_pali_to_roman(extract(clean(pada.pada)))

            child_pada.save()
            messages.success(self.request, _('The record has been added!'))
            
            return redirect(request.get_full_path())
        return render(request, self.template_name, {'form': form, 'pada': pada})


# -----------------------------------------------------
# PadaDuplicateView
# -----------------------------------------------------
class PadaDuplicateView(View, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    def get(self, request, padanukkama_id, pk):
        # Retrieve the Pada record to be duplicated
        try:
            pada = Pada.objects.get(id=pk, padanukkama_id=padanukkama_id)
        except Pada.DoesNotExist:
            # Handle the case where the Pada record is not found
            return redirect(reverse_lazy('padanukkama_pada', args=[padanukkama_id]))

        # Create a duplicate Pada record with a different ID
        clean_ex_pada=extract(clean(pada.pada))
        try:
            Pada.objects.create(
                padanukkama_id=pada.padanukkama_id,
                pada=pada.pada,
                pada_seq=encode(clean_ex_pada),
                pada_roman_script=cv_pali_to_roman(clean_ex_pada),
                parent=pada.parent,
            )
            messages.success(self.request, _('The record has been duplicated!'))
        except:
            messages.error(self.request, _('Error: Record duplication unsuccessful'))

        # Redirect to the edit page of the duplicated Pada record
        return redirect(reverse_lazy('padanukkama_pada', args=[padanukkama_id]))


# -----------------------------------------------------
# PadaDeclensionView
# -----------------------------------------------------
class PadaDeclensionView(View, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    template_name = 'padanukkama/pada_declension.html'

    def get(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, id=pk)
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        form = AddChildPadaForm()
        table = PadaParentChildTable(data=pada.get_current_with_descendants())
        message = _('Are you sure you want to delete this record?')

        return render(request, self.template_name, {'form': form, 'pada': pada, 'table':table, 'message':message})
    
    def post(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, id=pk)
        form = AddChildPadaForm(request.POST)
        if form.is_valid():
            child_pada = form.save(commit=False)
            child_pada.parent = pada
            child_pada.padanukkama = pada.padanukkama
            child_pada.pada_seq = encode(extract(clean(pada.pada)))
            child_pada.pada_roman_script = cv_pali_to_roman(extract(clean(pada.pada)))

            child_pada.save()
            messages.success(self.request, _('The record has been added!'))
            
            return redirect(request.get_full_path())
        return render(request, self.template_name, {'form': form, 'pada': pada})
    

# -----------------------------------------------------
# PadaDeleteView
# -----------------------------------------------------
class PadaDeleteView(View, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    def post(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, pk=pk)
        pada_parent_id = pada.parent_id
        try:
            pada.delete()
            messages.success(self.request, _('The record has been deleted!'))
        except:
            messages.error(self.request, _('Error: Record deletion unsuccessful'))
        
        if pada_parent_id is None:
            # Redirect to the padanukkama_pada view if parent_id is None
            return redirect('padanukkama_pada', padanukkama_id=padanukkama_id)
        else:
            # Redirect to the pada_split_sandhi view with parent_id as a positional argument
            return redirect(reverse_lazy('pada_split_sandhi', args=[padanukkama_id, pada_parent_id]))





class CreateSaddaView(View):
    def get(self, request):
        form = SaddaForm()
        linked_sadda_options = self.get_linked_sadda_options()
        linked_sadda_options_json = json.dumps(linked_sadda_options)  # Convert to JSON string
        return render(request, 'padanukkama/sadda_create.html', {'form': form, 'linked_sadda_options': linked_sadda_options_json})

    def post(self, request):
        form = SaddaForm(request.POST)
        if form.is_valid():
            sadda = form.save()
            return redirect('sadda_detail', pk=sadda.pk)
        linked_sadda_options = self.get_linked_sadda_options()
        linked_sadda_options_json = json.dumps(linked_sadda_options)  # Convert to JSON string
        return render(request, 'padanukkama/sadda_create.html', {'form': form, 'linked_sadda_options': linked_sadda_options_json})
    
    def get_linked_sadda_options(self):
        linked_sadda_options = {
            'NamaSaddamala': [],
            'AkhyataSaddamala': []
        }
        
        # Retrieve the options for NamaSaddamala
        nama_saddamala_options = NamaSaddamala.objects.all().values_list('id', 'title')
        linked_sadda_options['NamaSaddamala'] = [{'value': id, 'label': title} for id, title in nama_saddamala_options]
        
        # Retrieve the options for AkhyataSaddamala
        akhyata_saddamala_options = AkhyataSaddamala.objects.all().values_list('id', 'title')
        linked_sadda_options['AkhyataSaddamala'] = [{'value': id, 'label': title} for id, title in akhyata_saddamala_options]
        
        return linked_sadda_options

class SaddaDetailView(View):
    def get(self, request, pk):
        sadda = Sadda.objects.get(pk=pk)
        return render(request, 'padanukkama/sadda_detail.html', {'sadda': sadda})