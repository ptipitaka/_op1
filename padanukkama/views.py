from braces import views

import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import resolve, reverse_lazy

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from fuzzywuzzy import fuzz, process

from mptt.exceptions import InvalidMove

from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama, Pada, Sadda, \
                    NamaType, Linga, Karanta, Dhatu, Paccaya

from abidan.models import Word, WordLookup

from .tables import NamaSaddamalaTable, \
                    NamaSaddamalaFilter, AkhyataSaddamalaTable, \
                    AkhyataSaddamalaFilter, PadanukkamaTable, \
                    PadanukkamaFilter, PadaTable, PadaFilter, \
                    PadaParentChildTable

from .forms import  NamaSaddamalaForm, AkhyataSaddamalaForm, \
                    PadanukkamaCreateForm, PadanukkamaUpdateForm, \
                    AddChildPadaForm, \
                    PadaForm

from utils.pali_char import *
from utils.padanukkama import *

# -----------------------------------------------------
# NamaSaddamalaView
# -----------------------------------------------------
class NamaSaddamalaView(SingleTableMixin, FilterView):
    login_required = True
    superuser_required = True

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
class NamaSaddamalaCreateView(CreateView):
    login_required = True
    superuser_required = True

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
class NamaSaddamalaUpdateView(UpdateView):
    login_required = True
    superuser_required = True

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
class NamaSaddamalaDeleteView(DeleteView):
    login_required = True
    superuser_required = True

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
class AkhyataSaddamalaCreateView(CreateView):
    login_required = True
    superuser_required = True

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
class AkhyataSaddamalaUpdateView(UpdateView):
    login_required = True
    superuser_required = True

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
class AkhyataSaddamalaDeleteView(DeleteView):
    login_required = True
    superuser_required = True

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
class PadanukkamaCreateView(CreateView):
    login_required = True
    superuser_required = True

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
class PadanukkamaUpdateView(UpdateView):
    login_required = True
    superuser_required = True

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
class PadanukkamaDeleteView(DeleteView):
    login_required = True
    superuser_required = True

    model = Padanukkama
    success_url = reverse_lazy('padanukkama')
    template_name = "padanukkama/padanukkama_delete.html"


# -----------------------------------------------------
# PadanukkamaPadaView
# -----------------------------------------------------
class PadanukkamaPadaView(SingleTableMixin, FilterView):
    login_required = True
    superuser_required = True

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
class PadaSplitSandhiView(View):
    login_required = True
    superuser_required = True

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
class PadaDuplicateView(View):
    login_required = True
    superuser_required = True

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
class FindAbidanClosestMatchesView(View):
    def get(self, request):
        string = request.GET.get('string')  # Get the string from the AJAX request
        threshold = 70  # Set your desired threshold

        words = Word.objects.values_list('word', flat=True)  # Retrieve only the 'word' field
        matches = process.extractBests(string, words, scorer=fuzz.ratio, score_cutoff=threshold)
        matches_by_score = [{'match': match, 'score': score} for match, score in matches]
        match_array = [item['match'] for item in matches_by_score]

        serialized = {}
        if matches_by_score:
            word_queryset = Word.objects.filter(word__in=match_array).values_list('id', 'word', 'burmese')
            serialized = {word: {'id': id, 'word': word, 'burmese': burmese} for id, word, burmese in word_queryset}

        merged_results = []
        for item in matches_by_score:
            match = item['match']
            serialized_item = serialized.get(match)
            if serialized_item:
                # WordLookup
                wordlookup_queryset = WordLookup.objects.filter(word=serialized_item['word'])
                dict_array = list(wordlookup_queryset.values_list('dict', flat=True))
                
                serialized_item['dict'] = ', '.join(dict_array)
                serialized_item['score'] = item['score']
                
                word_id = serialized_item['id'] 
                word_instance = Word.objects.get(id=word_id)
                serialized_item['burmese'] = word_instance.burmese  # Retrieve the 'burmese' field from the Word instance
                serialized_item['image_ref'] = word_instance.image_ref()  # Add the image URL link
                
                merged_results.append(serialized_item)



        data = {
            'closest_matches': merged_results,
        }

        return JsonResponse(data)


# -----------------------------------------------------
# FindSaddaClosestMatchesView
# -----------------------------------------------------
class FindSaddaClosestMatchesView(View):
    def get(self, request):
        string = request.GET.get('string')  # Get the string from the AJAX request
        threshold = 70  # Set your desired threshold

        saddas = Sadda.objects.values_list('sadda', flat=True)  # Retrieve only the 'sadda' field
        matches = process.extractBests(string, saddas, scorer=fuzz.ratio, score_cutoff=threshold)
        closest_matches = [{'match': match, 'score': score} for match, score in matches]
        match_array = [item['match'] for item in closest_matches]

        serialized_queryset = {}
        if closest_matches:
            closest_matches_queryset = Sadda.objects.filter(sadda__in=match_array).values_list('id', 'sadda')
            serialized_queryset = {sadda: {'id': id, 'sadda': sadda} for id, sadda in closest_matches_queryset}

        merged_results = []
        for item in closest_matches:
            match = item['match']
            serialized_item = serialized_queryset.get(match)
            if serialized_item:
                serialized_item['score'] = item['score']
                merged_results.append(serialized_item)

        data = {
            'closest_matches': merged_results,
        }

        return JsonResponse(data)



# -----------------------------------------------------
# PadaDeclensionView
# -----------------------------------------------------
class PadaDeclensionView(View):
    login_required = True
    superuser_required = True
    template_name = 'padanukkama/pada_declension.html'

    def get(self, request, pk, padanukkama_id):
        pada = get_object_or_404(Pada, id=pk)
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        form = PadaForm(initial={'sadda': pada.pada})
        context = {
            'pada_id': pk,
            'pada': pada,
            'padanukkama_id': padanukkama_id,
            'padanukkama': padanukkama,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, padanukkama_id):
        pada = get_object_or_404(Pada, id=pk)
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        form = PadaForm(request.POST)
        if form.is_valid():
            # Process the form data
            # ...
            return redirect('success-url')
        context = {
            'pada_id': pk,
            'pada': pada,
            'padanukkama_id': padanukkama_id,
            'padanukkama': padanukkama,
            'form': form
        }
        return render(request, self.template_name, context)


# -----------------------------------------------------
# CreateVipatti
# -----------------------------------------------------
class CreateVipatti(View):
    def get(self, request, template_id, sadda):
        if not template_id or not sadda:
            return JsonResponse({'data': ''})
        
        sadda_type = template_id.split('_')[0]
        tid = template_id.split('_')[1]
        result = None
        if sadda_type == 'namasaddamala':
            result = mix_namavipatties(sadda, tid)
            template = NamaSaddamala.objects.get(pk=tid)
            template_data = {
                'title': template.title,
                'nama_type': template.nama_type.title if template.nama_type else '-',
                'linga': template.linga.title if template.linga else '-',
            }
        elif sadda_type == 'akhyatasaddamala':
            result = mix_akhyatavipatties(sadda, tid)
            template = AkhyataSaddamala.objects.get(pk=tid)
            template_data = {
                'title': template.title,
                'dhatu': template.dhatu.title if template.dhatu else '-',
                'paccaya': template.paccaya.title if template.paccaya else '-',
            }

        # Convert template object to dictionary

        data = {
            'result': result,
            'sadda_type': sadda_type,
            'template_data': template_data
        }

        return JsonResponse(data)

    
    
# -----------------------------------------------------
# PadaDeleteView
# -----------------------------------------------------
class PadaDeleteView(View):
    login_required = True
    superuser_required = True

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



# -----------------------------------------------------
# SaddaView
# -----------------------------------------------------
class CreateSaddaView(View):
    def get(self, request, padanukkama_id, pada_id):
        form = SaddaForm()
        linked_sadda_options = self.get_linked_sadda_options()
        linked_sadda_options_json = json.dumps(linked_sadda_options)  # Convert to JSON string
        
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        pada = get_object_or_404(Pada, id=pada_id)

        return render(
            request,
            'padanukkama/sadda_create.html',
            {
                'form': form,
                'linked_sadda_options': linked_sadda_options_json,
                'padanukkama': padanukkama,
                'pada': pada
            })

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
        nama_saddamala_options = NamaSaddamala.objects.all().order_by('title_order').values_list('id', 'title', 'linga__code')
        linked_sadda_options['NamaSaddamala'] = [{'value': id, 'label': f"{title} ({linga__code})"} for id, title, linga__code in nama_saddamala_options]
        
        # Retrieve the options for AkhyataSaddamala
        akhyata_saddamala_options = AkhyataSaddamala.objects.all().values_list('id', 'title')
        linked_sadda_options['AkhyataSaddamala'] = [{'value': id, 'label': f"{title} ({linga})"} for id, title, linga in akhyata_saddamala_options]

        return linked_sadda_options

class SaddaDetailView(View):
    def get(self, request, pk):
        sadda = Sadda.objects.get(pk=pk)
        return render(request, 'padanukkama/sadda_detail.html', {'sadda': sadda})
    
