import threading
import random

from braces import views
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from utils.pali_char import *
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2.views import SingleTableMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from mptt.utils import tree_item_iterator

from .models import Edition, Page, WordlistVersion, WordList, TableOfContent, Structure
from .tables import DigitalArchiveTable, TocTable, StructureTable, StructureFilter
from .forms import QForm, EditForm, WLGForm


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
        structure_slug = self.kwargs.get('slug')
        structure = get_object_or_404(Structure, slug=structure_slug)
        common_refs = structure.commonreference_set.all()
        context['structure'] = structure
        context['common_refs'] = common_refs
        context['form'] = CommonReferenceForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     structure_id = self.kwargs['id']
    #     structure = get_object_or_404(Structure, id=structure_id)
    #     common_refs = structure.commonreference_set.all()
    #     form = CommonReferenceForm(request.POST)
    #     if form.is_valid():
    #         common_ref = form.save(commit=False)
    #         common_ref.structure = structure
    #         common_ref.save()
    #         return redirect('common_reference_subform', id=structure_id)
    #     return self.render_to_response({'structure': structure, 'common_refs': common_refs, 'form': form})


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

