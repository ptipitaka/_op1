import threading

from braces import views
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django.shortcuts import render, redirect
from django_tables2.views import SingleTableMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import UpdateView
from mptt.templatetags.mptt_tags import cache_tree_children
from mptt.utils import tree_item_iterator
from utils.pali_char import clean, extract, encode

from .models import Edition, Page, WordlistVersion, WordList, TableOfContent, Structure
from .tables import DigitalArchiveTable, TocTable, StructureTable, StructureFilter
from .forms import QForm, EditForm, WLGForm



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



class TocTreeView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, SingleTableMixin, FilterView):
    model = Structure
    template_name = "tipitaka/toc-details.html"
    context_object_name  = "tocs"
    table_class = StructureTable
    filterset_class = StructureFilter

    def get_context_data(self, **kwargs):
        context = super(TocTreeView, self).get_context_data(**kwargs)
        context["total_rec"] = '{:,}'.format(len(self.get_table().rows)) 
        return context



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