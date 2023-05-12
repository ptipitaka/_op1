from braces import views
from django_filters.views import FilterView
from django.shortcuts import get_object_or_404
from django_tables2.views import SingleTableMixin
from django.urls import resolve, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama
from tipitaka.models import TableOfContent
from .tables import NamaSaddamalaTable, NamaSaddamalaFilter, AkhyataSaddamalaTable, AkhyataSaddamalaFilter, PadanukkamaTable, PadanukkamaFilter
from .forms import NamaSaddamalaForm, AkhyataSaddamalaForm, PadanukkamaCreateForm, PadanukkamaUpdateForm


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


class NamaSaddamalaCreateView(CreateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala_detail.html"
    form_class = NamaSaddamalaForm
    success_url = reverse_lazy('nama_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


class NamaSaddamalaUpdateView(UpdateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala_detail.html"
    form_class = NamaSaddamalaForm
    success_url = reverse_lazy('nama_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


class NamaSaddamalaDeleteView(DeleteView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = NamaSaddamala
    template_name = "padanukkama/nama_saddamala_detail.html"
    success_url = reverse_lazy('nama_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nama_saddamala'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


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


class AkhyataSaddamalaCreateView(CreateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala_detail.html"
    form_class = AkhyataSaddamalaForm
    success_url = reverse_lazy('akhyata_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


class AkhyataSaddamalaUpdateView(UpdateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala_detail.html"
    form_class = AkhyataSaddamalaForm
    success_url = reverse_lazy('akhyata_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


class AkhyataSaddamalaDeleteView(DeleteView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = AkhyataSaddamala
    template_name = "padanukkama/akhyata_saddamala_detail.html"
    success_url = reverse_lazy('akhyata_saddamala')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['akhyata_saddamala'] = self.get_object()
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


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


class PadanukkamaCreateView(CreateView, views.LoginRequiredMixin, views.SuperuserRequiredMixin):
    model = Padanukkama
    template_name = "padanukkama/padanukkama_create.html"
    form_class = PadanukkamaCreateForm, PadanukkamaUpdateForm
    success_url = reverse_lazy('padanukkama_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = resolve(self.request.path_info).url_name
        return context


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
        context['url_name'] = resolve(self.request.path_info).url_name

        return context