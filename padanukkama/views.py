import inspect

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.urls import resolve, reverse_lazy

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from fuzzywuzzy import fuzz, process
from simple_history.utils import get_history_manager_for_model
from tablib import Dataset
from urllib.parse import urlencode

from .models import NamaSaddamala, Padanukkama, Pada, Sadda

from abidan.models import Word, WordLookup

from .tables import NamaSaddamalaTable, NamaSaddamalaFilter, \
                    PadanukkamaTable, PadanukkamaFilter, \
                    PadaTable, PadaFilter, \
                    PadaParentChildTable, \
                    SaddaTable, SaddaFilter

from .forms import  NamaSaddamalaForm, \
                    PadanukkamaCreateForm, PadanukkamaUpdateForm, \
                    AddChildPadaForm, SaddaForm, ExportSaddaForm

from .admin import SaddaResource

from utils.pali_char import *
from utils.padanukkama import *
from utils.declension import *

# ====================================================
# NamaSaddamala
# ====================================================

# NamaSaddamalaView
#------------------
class NamaSaddamalaView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala.html"
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
    template_name = "padanukkama/nama_saddamala_detail.html"
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
    template_name = "padanukkama/nama_saddamala_detail.html"
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
    template_name = "padanukkama/nama_saddamala_detail.html"
    success_url = reverse_lazy('nama_saddamala')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nama_saddamala'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context



# ====================================================
# Padanukkama
# ====================================================

# PadanukkamaView
# ---------------
class PadanukkamaView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Padanukkama
    template_name = "padanukkama/padanukkama.html"
    context_object_name  = "padanukkama"
    table_class =PadanukkamaTable
    filterset_class =PadanukkamaFilter
    
    def get_context_data(self, **kwargs):
        context = super(PadanukkamaView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context



# PadanukkamaCreateView
# ---------------------
class PadanukkamaCreateView(SuperuserRequiredMixin, CreateView):
    model = Padanukkama
    template_name = "padanukkama/padanukkama_create.html"
    form_class = PadanukkamaCreateForm

    def handle_no_permission(self, request):
        messages.error(request, _('You do not have permission to access this page'))
        return redirect_to_login(request.get_full_path(), login_url=self.get_login_url(), redirect_field_name=self.get_redirect_field_name())

    def get_success_url(self):
        return reverse_lazy('padanukkama_update', args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# PadanukkamaUpdateView
# ---------------------
class PadanukkamaUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Padanukkama
    context_object_name = 'padanukkama'
    template_name = "padanukkama/padanukkama_update.html"
    form_class = PadanukkamaUpdateForm
    success_url = reverse_lazy('padanukkama')

    def handle_no_permission(self, request):
        messages.error(request, _('You do not have permission to access this page'))
        return redirect_to_login(request.get_full_path(), login_url=self.get_login_url(), redirect_field_name=self.get_redirect_field_name())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['table_of_content'] = self.object.table_of_content
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, _('Form is invalid. Please correct the errors.'))
        return super().form_invalid(form)



# PadanukkamaDeleteView
# ---------------------
class PadanukkamaDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Padanukkama
    success_url = reverse_lazy('padanukkama')
    template_name = "padanukkama/padanukkama_delete.html"

    def handle_no_permission(self, request):
        messages.error(request, _('You do not have permission to access this page'))
        return redirect_to_login(request.get_full_path(), login_url=self.get_login_url(), redirect_field_name=self.get_redirect_field_name())



# =====================================================
# PadanukkamaPadaView
# =====================================================
class PadanukkamaPadaView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Pada
    template_name = "padanukkama/pada.html"
    context_object_name = 'pada'
    table_class = PadaTable
    filterset_class = PadaFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Call the parent get() method to get the initial queryset and set up the filter
        response = super().get(request, *args, **kwargs)
        padanukkama_id = self.kwargs.get('padanukkama_id')
        # Access the page_number from the filter instance
        page_number = self.filterset.page_number

        # Check if a redirect is needed
        if page_number is not None:
            # Redirect to the page corresponding to the page_number
            redirect_url = reverse('padanukkama_pada', args=[padanukkama_id])
            redirect_url += f'?page={page_number}'
            return HttpResponseRedirect(redirect_url)

        return response
    
    def get_queryset(self):
        queryset = super().get_queryset()
        padanukkama_id = self.kwargs.get('padanukkama_id')
        padanukkama = get_object_or_404(Padanukkama, pk=padanukkama_id)
        queryset = Pada.objects.filter(padanukkama=padanukkama)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        padanukkama_id = self.kwargs['padanukkama_id']
        context["padanukkama_id"] = padanukkama_id
        context['deleted_conf_message'] = _('Are you sure you want to delete this record?')
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        history_manager = get_history_manager_for_model(Sadda)
        try:
            last_sadda_updated = history_manager.filter(
                history_user=self.request.user).latest('history_date')
            # Get the related Pada object from the last_sadda_updated
            sadda=Sadda.objects.filter(sadda=last_sadda_updated.sadda).first()
            if sadda:
                last_sadda_pada = Pada.objects.get(sadda=sadda.id)
                context['last_sadda_pada'] = last_sadda_pada
            else:
                context['last_sadda_pada'] = None
        except:
            context['last_sadda_pada'] = None

        return context

    def get_page_url(self, page_number):
        url = self.request.get_full_path()
        return f"{url}?page={page_number}"



# PadaSplitSandhiView
# -------------------
class PadaSplitSandhiView(LoginRequiredMixin, View):
    template_name = 'padanukkama/pada_split_sandhi.html'
    
    def get(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, id=pk)
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        form = AddChildPadaForm()

        table = PadaParentChildTable(
            data=pada.get_current_with_descendants(),
            request=request)

        return render(request, self.template_name, {'form': form, 'pada': pada, 'table':table})
    
    def post(self, request, padanukkama_id, pk):
        pada = get_object_or_404(Pada, id=pk)
        padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)
        form = AddChildPadaForm(request.POST)
        
        if form.is_valid():
            existing_pada = Pada.objects.filter(
                Q(pada=form.cleaned_data['pada']),
                Q(padanukkama=padanukkama)
            ).first()
            
            child_pada = form.save(commit=False)
            child_pada.parent = pada
            child_pada.padanukkama = pada.padanukkama
            child_pada.pada_seq = encode(extract(clean(pada.pada)))
            child_pada.pada_roman_script = cv_pali_to_roman(extract(clean(pada.pada)))

            if existing_pada:
                child_pada.sadda = existing_pada.sadda
            
            child_pada.save()
            messages.success(self.request, _('The record has been added!'))
            
            return redirect(request.get_full_path())
        return render(request, self.template_name, {'form': form, 'pada': pada})



# PadaDuplicateView
# -----------------
class PadaDuplicateView(LoginRequiredMixin, View):
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

        # Redirect to the desired URL with the page query parameter
        redirect_url = reverse_lazy('padanukkama_pada', args=[padanukkama_id]) + '?' + request.GET.urlencode()
        return redirect(redirect_url)



# PadaDeleteView
# --------------
class PadaDeleteView(SuperuserRequiredMixin, View):
    def handle_no_permission(self, request):
        messages.error(request, _('You do not have permission to access this page'))
        return redirect_to_login(request.get_full_path(), login_url=self.get_login_url(), redirect_field_name=self.get_redirect_field_name())

    def get(self, request, padanukkama_id, pk):
        # Retrieve the Pada record to be delete
        pada = get_object_or_404(Pada, pk=pk)
        pada_parent_id = pada.parent_id
        try:
            pada.delete()
            messages.success(self.request, _('The record has been deleted!'))
        except:
            messages.error(self.request, _('Error: Record deletion unsuccessful'))
        
        if pada_parent_id:
            redirect_url = reverse_lazy('pada_split_sandhi', args=[padanukkama_id, pada_parent_id]) + '?' + request.GET.urlencode()
        else:
            redirect_url = reverse_lazy('padanukkama_pada', args=[padanukkama_id]) + '?' + request.GET.urlencode()

        # Redirect to the desired URL with the page query parameter
        return redirect(redirect_url)



# FindAbidanClosestMatchesView
# ----------------------------
class FindAbidanClosestMatchesView(LoginRequiredMixin, View):
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



# FindSaddaClosestMatchesView
# ---------------------------
class FindSaddaClosestMatchesView(LoginRequiredMixin, View):
    def get(self, request):
        string = request.GET.get('string')  # Get the string from the AJAX request
        threshold = 70  # Set your desired threshold

        saddas = Sadda.objects.values_list('sadda', flat=True)  # Retrieve only the 'sadda' field
        matches = process.extractBests(string, saddas, scorer=fuzz.ratio, score_cutoff=threshold)
        closest_matches = [{'match': match, 'score': score} for match, score in matches]
        match_array = [item['match'] for item in closest_matches]

        serialized_queryset = {}
        if closest_matches:
            closest_matches_queryset = Sadda.objects.filter(sadda__in=match_array).values_list('id', 'sadda', 'construction')
            serialized_queryset = {sadda: {'id': id, 'sadda': sadda, 'construction': construction} for id, sadda, construction in closest_matches_queryset}

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



# PadaDeclensionView
# ------------------
class PadaDeclensionView(LoginRequiredMixin, View):
    template_name = 'padanukkama/pada_declension.html'
    
    def get(self, request, padanukkama_id, pk):
        try:
            pada = get_object_or_404(Pada, id=pk)
            padanukkama = get_object_or_404(Padanukkama, id=padanukkama_id)

            if pada.sadda:
                # Get sadda object & assign Form
                initial_data = {
                    'padanukkama': pada.padanukkama,
                    'sadda':  pada.sadda.sadda,
                    'sadda_type':  pada.sadda.sadda_type,
                    'namasaddamala': [item.pk for item in pada.sadda.namasaddamala.all()],
                    'construction':  pada.sadda.construction,
                    'description': pada.sadda.description
                }
                form = SaddaForm(initial = initial_data)
            else:
                # Initial blank form 
                form = SaddaForm(initial={
                    'padanukkama': pada.padanukkama,
                    'sadda': pada.pada,
                    'sadda_type': 'Nama'
                })

            context = {
                'pada_id': pk,
                'pada': pada,
                'padanukkama_id': padanukkama_id,
                'padanukkama': padanukkama,
                'form': form,
            }

            return render(request, self.template_name, context)
       
        except ObjectDoesNotExist as e:
            line_number = inspect.currentframe().f_lineno
            error_message = _('Error: {}-{}, please contact SA').format(line_number, e)
            messages.error(request, error_message)
            return render(request, self.template_name, context)
    
    def post(self, request, padanukkama_id, pk):
        pada = Pada.objects.get(id=pk)
        padanukkama = Padanukkama.objects.get(id=padanukkama_id)
        
        # Check if the form is for update or create
        if pada.sadda:
            form = SaddaForm(request.POST or None, instance=pada.sadda)
        else:
            form = SaddaForm(request.POST or None)

        if form.is_valid():
            existing_sadda = Sadda.objects.filter(
                Q(sadda=form.cleaned_data['sadda']),
                Q(padanukkama=padanukkama)
            ).first()

            if existing_sadda:
                form = SaddaForm(request.POST or None, instance=existing_sadda)
            
            # Form is valid, save the data
            sadda = form.save(commit=False)
            sadda.padanukkama = padanukkama
            sadda.save()
            form.save_m2m()

            # Update popularity of namasaddamala
            for e in sadda.namasaddamala.all():
                e.popularity += 1
                e.save()

            # Update Pada
            pada.sadda = sadda
            pada.save()


            # Find all related Pada
            if sadda.sadda_type == 'Nama':
                template_ids = list(sadda.namasaddamala.all())
                value_list = []
                for tid in template_ids:
                    result = noun_declension(sadda.sadda, tid.id)

                for key, value in result.items():
                    if key != 'error':
                        value_list.extend(value.split())
                unique_words = set(value_list)

                padas_to_update = Pada.objects.filter(padanukkama=padanukkama, pada__in=unique_words)
                for pada in padas_to_update:
                    # Update the object based on your requirements
                    pada.sadda = sadda
                    # Save the changes
                    pada.save()

            # Finished process
            messages.success(request, _('Record updated successfully!'))

            # Redirect to the desired URL with the page query parameter
            redirect_url = reverse_lazy('padanukkama_pada', args=[padanukkama_id]) + '?' + request.GET.urlencode()
            return redirect(redirect_url)

        else:
            # Invalid form, Message
            messages.error(request, _('Form is invalid. Please correct the errors'))
        
        # Re-render the page with form and other context data
        context = {
            'pada_id': pk,
            'pada': pada,
            'padanukkama_id': padanukkama_id,
            'padanukkama': padanukkama,
            'form': form,
        }
        
        return render(request, self.template_name, context)



# FindExistingSadda
# -----------------
class FindExistingSadda(LoginRequiredMixin, View):
    def get(self, request, padanukkama_id, sadda):
        existing_sadda = Sadda.objects.filter(Q(padanukkama=padanukkama_id), Q(sadda=sadda)).first()
        if existing_sadda:
            data = {
                'found': True,
                'existing_sadda_id': existing_sadda.id,
            }
        else:
            data = {
                'found': False,
            }
        
        return JsonResponse(data)



# AddSaddaToPada
# --------------
class AddSaddaToPada(LoginRequiredMixin, View):
    def post(self, request, padanukkama_id, pada_id, sadda_id):
        # Retrieve the current pada record
        current_pada = get_object_or_404(Pada, id=pada_id)
        current_sadda = get_object_or_404(Sadda, id=sadda_id)

        # Update the pada record with the sadda ID
        current_pada.sadda = current_sadda
        current_pada.save()

        return JsonResponse({'success': True})



# DecouplingPadaWithSadda
# -----------------------
class DecouplingPadaWithSadda(LoginRequiredMixin, View):
    def post(self, request, pada_id):
        # Retrieve the current pada record
        current_pada = get_object_or_404(Pada, id=pada_id)

        # Update the pada record with the sadda ID
        current_pada.sadda = None
        current_pada.save()

        return JsonResponse({'success': True})



# CreateVipatti
# -------------
class CreateVipatti(LoginRequiredMixin, View):
    def get(self, request, padanukkama_id, sadda, sadda_type, template_ids):
        if not template_ids or not sadda:
            return JsonResponse({'data': ''})
        
        template_ids = template_ids.split(',')
        result = None
        data = []

        if sadda_type == 'Nama':
            for tid in template_ids:
                result = noun_declension(sadda, tid)
                # result = mix_namavipatties(sadda, tid)
                template = NamaSaddamala.objects.get(pk=tid)
                template_data = {
                    'title': template.title,
                    'nama_type': template.nama_type.title if template.nama_type else '-',
                    'linga': template.linga.title if template.linga else '-',
                    'update_url': reverse_lazy('nama_saddamala_update', args=[tid]),
                }

                value_list = []
                for key, value in result.items():
                    if key != 'error':
                        value_list.extend(value.split()) 
                unique_words = set(value_list)

                padanukkama = Padanukkama.objects.get(id=padanukkama_id)
                wordlist_version_ids = padanukkama.wordlist_version.values_list('id', flat=True)

                wordlist_data = WordList.objects.filter(
                    wordlist_version__in=wordlist_version_ids,
                    word__in=unique_words
                ).values_list('word', flat=True).distinct()

                data.append({
                    'result': result,
                    'sadda_type': sadda_type,
                    'template_data': template_data,
                    'padas': list(wordlist_data)
                })

        return JsonResponse(data, safe=False)



# =====================================================
# SaddaView
# =====================================================

# SaddaView
# ---------
class SaddaView(LoginRequiredMixin, SingleTableMixin, FilterView, FormView):
    model = Sadda
    template_name = "padanukkama/sadda.html"
    context_object_name = "sadda"
    table_class = SaddaTable
    filterset_class = SaddaFilter
    form_class = ExportSaddaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        padanukkama_id = self.request.GET.get('padanukkama')
        context['padanukkama_id'] = padanukkama_id
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows))
        return context
    
    def get_queryset(self):
        # Get the original queryset
        queryset = super().get_queryset()
        
        # Apply the filter to the padanukkama field
        padanukkama_id = self.request.GET.get('padanukkama')
        if padanukkama_id:
            queryset = queryset.filter(padanukkama_id=padanukkama_id)
        
        return queryset

    def post(self, request, **kwargs):
        filter_form = self.get_form(self.form_class)
        if filter_form.is_valid():
            queryset = self.get_queryset()
            filterset = self.filterset_class(request.GET, queryset=queryset, request=request)
            filtered_queryset = filterset.qs
            dataset = SaddaResource().export(filtered_queryset)

            format = request.POST.get('format')

            if format == 'xls':
                ds = dataset.xls
            elif format == 'json':
                ds = dataset.json
            else:
                ds = dataset.csv

            response = HttpResponse(ds, content_type=f"{format}")
            response['Content-Disposition'] = f"attachment; filename=sadda.{format}"
            return response
    


# SaddaUpdateView
# ---------------
class SaddaUpdateView(LoginRequiredMixin, UpdateView):
    model = Sadda
    template_name = "padanukkama/sadda_update.html"
    form_class = SaddaForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sadda = self.get_object()
        context['padanukkama_id'] = sadda.padanukkama.id
        return context

    def get_initial(self):
        initial = super().get_initial()
        sadda = self.get_object()
        if sadda.padanukkama:
            initial['padanukkama'] = sadda.padanukkama
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Form saved successfully."))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = _("Form contains errors. Please correct them.")
        messages.error(self.request, error_message)
        return response
    
    def get_success_url(self):
        success_url = reverse_lazy('sadda')
        query_params = self.request.GET.copy()  # Create a mutable copy of the request's GET parameters
        success_url += '?' + urlencode(query_params)  # Add the query parameters to the success URL
        return success_url
    


# FindRelatedPadaView
# --------------------
class FindRelatedPadaView(LoginRequiredMixin, View):
    def get(self, request):
        sadda_id = int(request.GET.get('string'))  # Convert the string to an integer
        padas = list(set(Pada.objects.filter(sadda=sadda_id).values_list('pada', flat=True)))
        data = {
            'related_padas': padas,
        }

        return JsonResponse(data)
