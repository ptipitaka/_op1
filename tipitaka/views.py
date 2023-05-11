import threading

from braces import views
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2.views import SingleTableMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView, DetailView
from utils.pali_char import *

from .models import Edition, Page, WordlistVersion, WordList, TableOfContent, Structure, CommonReference
from .tables import DigitalArchiveTable, WordlistMasterTable, WordlistMasterFilter, TocTable, StructureTable, StructureFilter, WordListTable, CommonReferenceTable
from .forms import DigitalArchiveForm, EditForm, UpdWlAndPageForm, WLGForm, WordlistFinderForm


# ----------------------------------------------------------------
# TIPITAKA DIGITAL ARCHIVED
# ----------------------------------------------------------------

class DigitalArchiveView(View):
    def get(self, request):
        form = DigitalArchiveForm(request.GET)
        
        edition = request.GET.get('edition')
        volume = request.GET.get('volume', '')
        page_number = request.GET.get('page_number', '')
        content = request.GET.get('content', '')

        queryset = Page.objects.filter(
            edition=edition,
        )

        if volume:
            queryset = queryset.filter(volume=volume)
        if content:
            queryset = queryset.filter(content__contains=content)
        if page_number:
            queryset = queryset.filter(page_number=page_number)

        queryset = queryset.order_by('edition', 'volume', 'page_number')

        table = DigitalArchiveTable(queryset)
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        total_rec = '{:,}'.format(table.page.paginator.count)

        return render(request, "tipitaka/digital_archive.html", {
            "form": form,
            'table': table,
            'total_rec': total_rec
        })


class DigitalArchiveDetialsView(SuccessMessageMixin, UpdateView):
    template_name = "tipitaka/digital_archive_details.html"
    model = Page
    form_class = EditForm
    success_message = _('Update successfully!')

    def get_success_url(self):
        edition = int(self.request.GET.get('edition'))
        volume = int(self.request.GET.get('volume'))
        page = int(self.request.GET.get('page')  or 1)
        return '/inscriber/digital-archive?edition=%s&volume=%s&page=%s' %(edition, volume, page)


class WordListView(SingleTableMixin, FilterView):
    model = WordList
    template_name = "tipitaka/wordlist-master.html"
    context_object_name  = "wordlist"
    table_class = WordlistMasterTable
    filterset_class = WordlistMasterFilter

    def get_context_data(self, **kwargs):
        context = super(WordListView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


class WordListPageSourceView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, UpdateView):
    model = WordList
    template_name = "tipitaka/wordlist-page-source.html"
    form_class = UpdWlAndPageForm
    success_url = reverse_lazy('wordlist_master')

    def get_success_url(self):
        return self.request.path

# ----------------------------------------------------------------
# TABLE OF CONTENTS & COMMON REFERENCE
# ----------------------------------------------------------------
class TocView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):

    def get(self, request):

        queryset = TableOfContent.objects.all().order_by('code',)
        table = TocTable(queryset)
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        total_rec = '{:,}'.format(table.page.paginator.count)

        return render(request, "tipitaka/toc.html", {
            'table': table,
            'total_rec': total_rec
        })
    def post(self, request):
        pass


class StructureView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, SingleTableMixin, FilterView):
    model = Structure
    template_name = "tipitaka/structure.html"
    context_object_name  = "tocs"
    table_class = StructureTable
    filterset_class = StructureFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        table_of_content = get_object_or_404(TableOfContent, slug=slug)
        queryset = Structure.objects.filter(table_of_content=table_of_content)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StructureView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context


class CommonReferenceSubformView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, TemplateView):
    template_name = "tipitaka/common_reference_subform.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get kwargs
        structure_id = self.kwargs['structure_id']
        
        # get Structure & Common Reference related to this structure
        structure = get_object_or_404(Structure, id=structure_id)
        structure_tree = structure.get_children()

        # context data and form
        context['structure'] = structure
        context['structure_tree'] = structure_tree
        context['page'] = ''
        context['no_data_in_common_ref_table'] = ''
        context['error_message'] = ''

        # table
        context['wordlist_table'] = []
        context['common_ref_table'] = CommonReferenceTable(structure.commonreference_set.all())
        if len(context['common_ref_table'].rows) == 0:
            context['no_data_in_common_ref_table'] = _('No common references found')
        
        # form
        context['WordlistFinderForm'] = WordlistFinderForm(structure_id=structure_id)

        # Accessing the fields
        fields = context['WordlistFinderForm'].fields
        context['edition_field'] = fields['edition']

        # return
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        structure_id = self.kwargs['structure_id']
        form = WordlistFinderForm(request.POST, structure_id = structure_id )

        if form.is_valid():
            if 'WordlistFinderForm_Search_Submit' in request.POST:
                page = Page.objects.get(id=request.POST['page'])
                wordlist_version = request.POST['wordlist_version']
                line_number = request.POST['line_number']
                if line_number == '0':
                    queryset = WordList.objects.filter(
                        wordlist_version=wordlist_version,
                        page=page
                    )
                else:
                    queryset = WordList.objects.filter(
                        wordlist_version=wordlist_version,
                        page=page,
                        line_number=line_number
                    )
                wordlist_table = WordListTable(queryset)
                context.update({
                    'wordlist_table': wordlist_table,
                    'page': page,
                })

            elif 'WordlistFinderForm_Add_or_Update' in request.POST:
                from_position_slug = request.POST.get('from_p')
                to_position_slug = request.POST.get('to_p')
                if from_position_slug and to_position_slug:
                    if from_position_slug < to_position_slug:
                        common_reference_exist = CommonReference.objects.filter(
                            Q(structure=kwargs['structure_id']) & 
                            Q(wordlist_version_id=request.POST['wordlist_version']))
                        if common_reference_exist:
                            # update the common reference object
                            common_reference_exist.update(
                                from_position=from_position_slug,
                                to_position=to_position_slug,
                            )
                        else:
                            # create a new common reference object
                            CommonReference.objects.create(
                                wordlist_version_id=request.POST['wordlist_version'],
                                structure_id=kwargs['structure_id'],
                                from_position=from_position_slug,
                                to_position=to_position_slug,
                            )
                        # redirect to same page to prevent duplicate form submissions
                        return redirect(request.path)
                else:
                  context.update({
                    'WordlistFinderForm': form,
                    'error_message': _('Invalid input. Please correct the errors below'),
                  })
                  return self.render_to_response(context)

        # handle errors by re-rendering the form with error messages
        context.update({
            'WordlistFinderForm': form,
            'error_message': _('Invalid input. Please correct the errors below'),
        })
        return self.render_to_response(context)


class CommonReferenceSubformDetailView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, DetailView):
    model = CommonReference
    template_name = "tipitaka/common_reference_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['from_wordlist_position'] = WordList.objects.get(code=self.object.from_position)
        context['from_wordlist_position'] = self.object.from_wordlist_position
        context['to_wordlist_position'] = self.object.to_wordlist_position
        context['all_wordlist_in_from_position_page'] = self.object.all_wordlist_in_from_position_page
        context['count_all_wordlist_in_from_position_page'] = self.object.count_all_wordlist_in_from_position_page
        return context

class CommonReferenceSubformDeleteView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, DeleteView):
    model = CommonReference
    template_name = 'tipitaka/common_reference_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['from_wordlist_position'] = WordList.objects.get(code=self.object.from_position)
        context['from_wordlist_position'] = self.object.from_wordlist_position
        context['to_wordlist_position'] = self.object.to_wordlist_position
        context['all_wordlist_in_from_position_page'] = self.object.all_wordlist_in_from_position_page
        context['count_all_wordlist_in_from_position_page'] = self.object.count_all_wordlist_in_from_position_page
        return context
    
    def get_success_url(self):
        # Customize the success URL based on some logic
        structure_id = self.kwargs['structure_id']
        return reverse_lazy(
            'common_reference_subform',
            kwargs={'slug': self.object.structure.table_of_content.slug, 'structure_id': structure_id})

