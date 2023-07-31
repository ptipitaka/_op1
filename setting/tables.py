import django_tables2 as tables

from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet, filters

from padanukkama.models import NamaSaddamala, NamaType, \
                    Karanta,Dhatugana, Dhatu, VerbConjugation, \
                    NounDeclension

from django_editorjs_parser import EditorJSParser
import json


# -----------------------------------------------------
# NamaSaddamala Table & Filter
# -----------------------------------------------------
class NamaSaddamalaTable(tables.Table):
    title_order = tables.Column(visible=False)
    popularity = tables.Column(visible=False)
    
    action = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name=_('Action'))
    
    def render_action(self, record):
        query_params = self.request.GET
        url = reverse_lazy('nama_saddamala_update', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'
        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
            f'<i class="fas fa-pencil-alt"></i></a>'
        )

    class Meta:
        model = NamaSaddamala
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("title_order", "title", "title_code", "linga", "karanta", "nama_type", "popularity",)
        order_by = ("-popularity", "title_order",)


class NamaSaddamalaFilter(FilterSet):
    title__contains = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Title contains'))
    nama_type__exact = filters.ChoiceFilter(
        field_name='nama_type',
        lookup_expr='exact',
        choices=NamaType.objects.values_list('id', 'title'),
        label=_('Type'))
    linga__exact = filters.ChoiceFilter(
        field_name='linga',
        lookup_expr='exact',
        choices=NamaType.objects.values_list('id', 'title'),
        label=_('Liṅga'))
    karanta__exact = filters.ChoiceFilter(
        field_name='karanta',
        lookup_expr='exact',
        choices=Karanta.objects.values_list('id', 'title'),
        label=_('Kāranta'))
    
    class Meta:
        model = NamaSaddamala
        fields = {}



# -----------------------------------------------------
# Dhatu Table & Filter
# -----------------------------------------------------
class DhatuTable(tables.Table):
    title_order = tables.Column(visible=False)
    popularity = tables.Column(visible=False)
    
    action = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name=_('Action'))
    
    def render_action(self, record):
        # Get all the query parameters from the request's GET parameters
        query_params = self.request.GET

        # Generate the URL with the updated parameters
        url = reverse_lazy('dhatu_update', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'
        
        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
            f'<i class="fas fa-pencil-alt"></i></a>'
        )

    class Meta:
        model = Dhatu
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("title_order", "title", "dhatugana", "paccaya", "definition", "meaning",)
        order_by = ("-popularity", "title_order",)


class DhatuFilter(FilterSet):
    title__contains = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Title contains'))
    dhatugana__exact = filters.ChoiceFilter(
        field_name='dhatugana',
        lookup_expr='exact',
        choices=Dhatugana.objects.values_list('id', 'title'),
        label=_('Dhatugana'))
    
    class Meta:
        model = Dhatu
        fields = {}



# -----------------------------------------------------
# NounDeclension Table & Filter
# -----------------------------------------------------
class NounDeclensionTable(tables.Table):
    action = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name=_('Action'))
    
    description = tables.Column(attrs={"td": {"style": "background-color: whitesmoke;"}})


    def render_action(self, record):
        # Get all the query parameters from the request's GET parameters
        query_params = self.request.GET

        # Generate the URL with the updated parameters
        url = reverse_lazy('noun_declension_update', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'

        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
            f'<i class="fas fa-pencil-alt"></i></a>'
        )

    def render_description(self, value):
        data = json.loads(value)
        parser = EditorJSParser()
        html_description = parser.parse(data)
        return mark_safe(html_description)

    class Meta:
        model = NounDeclension
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('code', 'title', 'description',)
        order_by = ("code",) 



class NounDeclensionFilter(FilterSet):
    code__exact = filters.CharFilter(
        field_name='code',
        lookup_expr='exact',
        label=_('Code'))
    title__contains = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Title contains'))
    
    class Meta:
        model = NounDeclension
        fields = {}



# -----------------------------------------------------
# VerbConjugation Table & Filter
# -----------------------------------------------------
class VerbConjugationTable(tables.Table): 
    action = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name=_('Action'))
    
    def render_action(self, record):
        # Get all the query parameters from the request's GET parameters
        query_params = self.request.GET

        # Generate the URL with the updated parameters
        url = reverse_lazy('verb_conjugation_update', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'
        
        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
            f'<i class="fas fa-pencil-alt"></i></a>'
        )

    class Meta:
        model = VerbConjugation
        template_name = "django_tables2/w3css.html"
        attrs = {
            "class": "w3-table w3-bordered",
            "th": {
                "style": "max-width: 300px;",
            },
            "td": {
                "style": "max-width: 300px;",
            },
            "td-description": {
                "style": "width: 300px; text-align: center;",
                "class": "custom-description-class",
            },
        }
        fields = ("title", "description", "meaning",)
        order_by = ("sequence",)


class VerbConjugationFilter(FilterSet):
    title__contains = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Title contains'))
    
    class Meta:
        model = VerbConjugation
        fields = {}