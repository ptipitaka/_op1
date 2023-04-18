import subprocess

from braces import views
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import UpdateView
# from django_rq import job

from tipitaka.models import Edition, Page, WordListVersion, WordList
from utils.pali_char import clean, extract, encode

from .tables import PagelistTable
from .forms import QForm, EditForm, WLGForm

class PageView(View):
    def get(self, request):
        form = QForm(request.GET)
        edition = request.GET.get('edition', None)
        volume = request.GET.get('volume', None)

        queryset = Page.objects.filter(edition=edition, volume=volume).order_by('edition', 'volume', 'page_number')
        table = PagelistTable(queryset)
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        total_wl = '{:,}'.format(table.page.paginator.count)

        return render(request, "tipitaka/digital-archive.html", {
            "form": form,
            'table': table,
            'total_wl': total_wl
        })
    def post(self, request):
        pass


class PageDetialsUpdateView(SuccessMessageMixin, UpdateView):
    template_name = "tipitaka/details.html"
    model = Page
    form_class = EditForm
    success_message = _('Update successfully!')

    def get_success_url(self):
        edition = int(self.request.GET.get('edition'))
        volume = int(self.request.GET.get('volume'))
        page = int(self.request.GET.get('page')  or 1)
        return '/inscriber/digital-archive?edition=%s&volume=%s&page=%s' %(edition, volume, page)

# @job
def q_create_wordlist(edition_id, created_by):
    try:
        # step 1 add WordListVersion
        edition_instance = Edition.objects.get(pk=edition_id)
        new_version_number = int(edition_instance.version) + 1
        # WordListVersion
        new_WordListVersion_instance = WordListVersion(
            version=new_version_number,
            edition=edition_instance
            )
        new_WordListVersion_instance.save(created_by=created_by)
        # Edition : update new version number
        edition_instance.version = new_version_number
        edition_instance.save()
        
        # step 2 create WordList and add to database related to lasted version
        all_pages = Page.objects.filter(edition=edition_id).order_by("volume", "page_number")[:10]
        for each_page in all_pages:
            position = 1
            line_number = 1
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
                            word = each_word,
                            word_seq = encode(extract(clean(each_word))),
                            position = position,
                            line_number = line_number,
                            wordlistversion = new_WordListVersion_instance,
                            edition = edition_instance,
                            volume = each_page.volume,
                            page = each_page,
                        )
                        new_wordlist_instance.save()

                        position += 1
                line_number += 1
        cache.set('task_status', 'done')
    except:
        print("ERROR : found error from q_create_wordlist")

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
        
        task_status = cache.get('task_status__q_create_wordlist')
        if task_status:
            if task_status == 'done':
                task_result = cache.get('task_result')
                cache.delete('task_status__q_create_wordlist')
                return render(request, self.template_name, {'task_result': task_result})
            else:
                return render(request, self.template_name, {'task_status': task_status})

        else:
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
            task_status: task_status,
        })

    def post(self, request, *args, **kwargs):
        form = WLGForm(request.POST)
        if form.is_valid():
            # Enqueue the task:
            edition_id = request.POST.get('edition')
            created_by = request.user
            # q_create_wordlist.delay(edition_id, created_by, request)
            cache.set('task_status__q_create_wordlist', 'waiting')

            messages.success(request, _("Enqueued task for create a new version of wordlist!"))
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
    
