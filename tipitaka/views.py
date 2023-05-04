import threading

from braces import views
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2.views import SingleTableMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView, DetailView
from mptt.utils import tree_item_iterator
from utils.pali_char import *

from .models import Edition, Page, WordlistVersion, WordList, TableOfContent, Structure, CommonReference
from .tables import DigitalArchiveTable, TocTable, StructureTable, StructureFilter, WordListTable, CommonReferenceTable
from .forms import QForm, EditForm, WLGForm, WordlistFinderForm


# ----------------------------------------------------------------
# TIPITAKA DIGITAL ARCHIVED
# ----------------------------------------------------------------

class DigitalArchiveView(View):
    def get(self, request):
        form = QForm(request.GET)
        edition = request.GET.get('edition', None)
        volume = request.GET.get('volume', None)

        queryset = Page.objects.filter(edition=edition, volume=volume).order_by('edition', 'volume', 'page_number')
        table = DigitalArchiveTable(queryset)
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        total_rec = '{:,}'.format(table.page.paginator.count)

        return render(request, "tipitaka/digital-archive.html", {
            "form": form,
            'table': table,
            'total_rec': total_rec
        })
    def post(self, request):
        pass

class DigitalArchiveDetialsView(SuccessMessageMixin, UpdateView):
    template_name = "tipitaka/digital-archive-details.html"
    model = Page
    form_class = EditForm
    success_message = _('Update successfully!')

    def get_success_url(self):
        edition = int(self.request.GET.get('edition'))
        volume = int(self.request.GET.get('volume'))
        page = int(self.request.GET.get('page')  or 1)
        return '/inscriber/digital-archive?edition=%s&volume=%s&page=%s' %(edition, volume, page)

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
        # Perform any necessary operations
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

            elif 'WordlistFinderForm_Add_Reference' in request.POST:
                from_position_slug = request.POST.get('from_p')
                to_position_slug = request.POST.get('to_p')
                if from_position_slug and to_position_slug:
                    if from_position_slug < to_position_slug:
                        CommonReference.objects.create(
                            wordlist_version_id=request.POST['wordlist_version'],
                            structure_id=kwargs['structure_id'],
                            from_position=from_position_slug,
                            to_position=to_position_slug,
                        )
                        # redirect to same page to prevent duplicate form submissions
                        return redirect(request.path)
                # if form is not valid or input is invalid, fall through to error handling

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

# ----------------------------------------------------------------
# UTILITIES
# ----------------------------------------------------------------

# Structures -----------------------------------------------------

def import_structure(structure_data):
    # Create a dictionary to map parent IDs to Sturcture instances
    parents = {}
    toc = TableOfContent.objects.get(pk=1)

    # Iterate over the structure data and create Sturcture instances
    for structure_data in structure_data:
        structure = Structure(
            code=structure_data['code'],
            title=structure_data['title'],
            ro=structure_data['ro'],
            si=structure_data['si'],
            hi=structure_data['hi'],
            lo=structure_data['lo'],
            my=structure_data['my'],
            km=structure_data['km'],
            table_of_content=toc)
        structure.parent = parents.get(structure_data['parent_id'])
        structure.save()

        # Add the new structure instance to the parent dictionary
        parents[structure_data['id']] = structure

    # Rebuild the tree structure
    tree_items = list(tree_item_iterator(Structure.objects.all()))
    Structure.objects.partial_rebuild(tree_items)

    return True

# define a function to update the code field recursively
@transaction.atomic
def update_structure_code(node):
    def create_code(title):
        print(title)
        payangka = get_first_payangka_roman(cv_payangka(extract(clean(title))), 9)
        return payangka

    siblings = node.get_siblings(include_self=True)
    code_array = [n.code for n in siblings]

    payangka = create_code(node.title)
    got_new_code = False
    if len(payangka) > 1:
        for i in range(0, len(payangka)):
            try:
                new_code = payangka[0] + payangka[i + 1]
                if new_code not in code_array:
                    print('adding code>1', new_code)
                    node.code = new_code
                    got_new_code = True
                    break
            except:
                if not got_new_code:
                    for i in range(1, 50):
                        new_code = payangka[0] + payangka[1] + str(i)
                        if new_code not in code_array:
                            print('adding code>1s', new_code)
                            node.code = new_code
                            break
    else:
        print(payangka)
        new_code = payangka[0]
        if new_code not in code_array:
            for i in range(1, 50):
                new_code = payangka[0] + str(i)
                if new_code not in code_array:
                    print('adding code=1', new_code)
                    node.code = new_code
                    break
    
    node.save()
    print(code_array)

    for child in node.get_children():
        update_structure_code(child)

# get the root node of the parent-child tree
# root_node = Structure.objects.get(parent=None)

# call the function to update the code field recursively
# update_structure_code(root_node)

# WordList -------------------------------------------------------

def create_wordlist_subprocess(edition_id, created_by):
    try:
        # step 1 add WordlistVersion
        edition_instance = Edition.objects.get(pk=edition_id)
        new_version_number = int(edition_instance.version) + 1
        # WordlistVersion
        new_WordlistVersion_instance = WordlistVersion(
            version=new_version_number,
            edition=edition_instance
            )
        new_WordlistVersion_instance.save(created_by=created_by)
        # Edition : update new version number
        edition_instance.version = new_version_number
        edition_instance.save()
        
        # step 2 create WordList and add to database related to lasted version
        all_pages = Page.objects.filter(edition=edition_id).order_by("volume", "page_number")
        for each_page in all_pages:
            position = 1
            line_number = 1
            if each_page.content:
                all_lines = each_page.content.replace("\r", "").split("\n")
                for each_line in all_lines:
                    all_words = each_line.split(" ")
                    for each_word in all_words:
                        cleaned_word = clean(each_word)
                        if len(cleaned_word.replace(" ", "")):
                            new_wordlist_instance = WordList(
                                code = "%s-%s-%s-%s" % (edition_instance.code,
                                                        str(each_page.volume.volume_number).zfill(3),
                                                        str(each_page.page_number).zfill(4),
                                                        str(position).zfill(3)),
                                word = cleaned_word,
                                word_seq = encode(extract(cleaned_word)),
                                position = position,
                                line_number = line_number,
                                wordlist_version = new_WordlistVersion_instance,
                                edition = edition_instance,
                                volume = each_page.volume,
                                page = each_page,
                            )
                            new_wordlist_instance.save()

                            position += 1
                    line_number += 1
        #     print('%s: %s' % (each_page.volume.volume_number, each_page.page_number))
        # print("DONE : create_wordlist of %s Successfully" % edition_instance.code)
    except:
        print("ERROR : found error from create_wordlist")

class WordlistGeneratorView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    #optional
    login_url = settings.LOGIN_URL

    template_name = "tipitaka/wordlist.html"
    success_url = reverse_lazy('wordlist_generator')

    def get(self, request, *args, **kwargs):
        form = WLGForm(request.GET)
        selected_edition_id = request.GET.get('edition')
        selected_edition = None
        new_version = None
        total_wordlist_in_current_version = None
        
        if selected_edition_id:
            selected_edition = Edition.objects.get(pk=selected_edition_id)
            new_version = int(selected_edition.version) + 1
            total_wordlist_in_current_version = WordList.objects.filter(edition=selected_edition_id).count()

        return render(request, self.template_name, {
            "form": form,
            "selected_edition_id": selected_edition_id,
            "selected_edition": selected_edition,
            "new_version": new_version,
            "total_wordlist_in_current_version": total_wordlist_in_current_version,
        })

    def post(self, request, *args, **kwargs):
        form = WLGForm(request.POST)
        if form.is_valid():
            # Enqueue the task:
            edition_id = request.POST.get('edition')
            created_by = request.user
            create_wordlist_subprocess(edition_id, created_by)
            t = threading.Thread(target=create_wordlist_subprocess, args=(edition_id, created_by))
            t.start()

            messages.success(request, _("Enqueued task for create a new version of wordlist!"))
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


def get_wordlist_versions(request, structure_id):
    structure = Structure.objects.get(id=structure_id)
    all_related_wordlist_versions = structure.table_of_content.wordlist_version.all()
    common_refs = CommonReference.objects.filter(structure=structure)
    all_added_wordlist_versions = WordlistVersion.objects.filter(commonreference__in=common_refs)
    remain_wordlist_version = all_related_wordlist_versions.exclude(pk__in=all_added_wordlist_versions.values_list('pk', flat=True))

    if structure:
        wordlist_versions = [{'pk':i.id, 'title':f"{i.edition.code} v.{i.version}"} for i in remain_wordlist_version] 
        return JsonResponse(wordlist_versions, safe=False)
        # wordlist_versions = remain_wordlist_version.values('pk', 'title') 
        # return JsonResponse(list(wordlist_versions), safe=False)
    return JsonResponse([], safe=False)