import django_filters
import django_tables2 as tables
from django import forms
from django_filters import FilterSet
from django_tables2.utils import A
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.templatetags.mptt_tags import cache_tree_children

from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama, Pada

class NamaSaddamalaTable(tables.Table):
    title_order = tables.Column(visible=False)
    action = tables.LinkColumn(
        viewname='nama_saddamala_update',
        args=[A('pk')],
        attrs={'class': 'w3-button'},
        text=mark_safe('<i class="fa-solid fa-magnifying-glass"></i>'),
        empty_values=(),
    )

    class Meta:
        model = NamaSaddamala
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("title", "title_order", "linga", "karanta",)
        order_by = ("title_order",)


class NamaSaddamalaFilter(FilterSet):
    class Meta:
        model = NamaSaddamala
        fields = ("title", "linga", "karanta",)


class AkhyataSaddamalaTable(tables.Table):
    title_order = tables.Column(visible=False)
    action = tables.LinkColumn(
        viewname='akhyata_saddamala_update',
        args=[A('pk')],
        attrs={'class': 'w3-button'},
        text=mark_safe('<i class="fa-solid fa-magnifying-glass"></i>'),
        empty_values=(),
    )

    class Meta:
        model = AkhyataSaddamala
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("title", "title_order", "dhatu", "paccaya",)
        order_by = ("title_order",)


class AkhyataSaddamalaFilter(FilterSet):
    class Meta:
        model = AkhyataSaddamala
        fields = ("title", "dhatu", "paccaya",)


class PadanukkamaTable(tables.Table):
    title_order = tables.Column(visible=False)
    action = tables.LinkColumn(
        viewname='padanukkama_update',
        args=[A('pk')],
        attrs={'class': 'w3-button'},
        text=mark_safe('<i class="fa-solid fa-magnifying-glass"></i>'),
        empty_values=(),
    )

    about = tables.Column(attrs={'td': {'style': 'width: 40%;'}})

    class Meta:
        model = Padanukkama
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("title", "about", "target_languages", "collaborators")
        order_by = ("title",)
    

class PadanukkamaFilter(FilterSet):

    publication = django_filters.BooleanFilter(
        label=_("Publication"),
        widget=forms.Select(
            choices=[(None, _("All")), (True, _("True")), (False, _("False"))]
        )
    )
    class Meta:
        model = Padanukkama
        fields = {
            "title": ["icontains"],
            "publication": ["exact"],
        }
        labels = {"title": _("Title"),}

class PadaTable(tables.Table):
    pada = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
        } 
    })

    class Meta:
        model = Pada
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('pada',)
        
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        
        ## Cache the tree Pada for performance ##
        cache_tree_children(data)

class PadaFilter(FilterSet):    
    class Meta:
        model = Pada
        fields = {"pada": ["contains"]}
