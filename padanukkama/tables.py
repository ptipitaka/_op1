import django_filters
import django_tables2 as tables
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_tables2.utils import A

from mptt.templatetags.mptt_tags import cache_tree_children

from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama, Pada

from django.utils.html import format_html

# -----------------------------------------------------
# NamaSaddamala Table & Filter
# -----------------------------------------------------
class NamaSaddamalaTable(tables.Table):
    title_order = tables.Column(visible=False)
    action = tables.LinkColumn(
        viewname='nama_saddamala_update',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=format_html('<i class="fa-solid fa-magnifying-glass"></i>'),
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
        fields = ("title", "nama_type", "linga", "karanta",)


# -----------------------------------------------------
# AkhyataSaddamala Table & Filter
# -----------------------------------------------------
class AkhyataSaddamalaTable(tables.Table):
    title_order = tables.Column(visible=False)
    action = tables.LinkColumn(
        viewname='akhyata_saddamala_update',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
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


# -----------------------------------------------------
# Padanukkama Table & Filter
# -----------------------------------------------------
class PadanukkamaTable(tables.Table):
    title_order = tables.Column(visible=False)
    update = tables.LinkColumn(
        viewname='padanukkama_update',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=mark_safe('<i class="fa-solid fa-magnifying-glass"></i>'),
        empty_values=(),
    )

    pada_list = tables.LinkColumn(
        viewname='padanukkama_pada',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=mark_safe('<i class="far fa-list"></i>'),
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


# -----------------------------------------------------
# Pada Table & Filter
# -----------------------------------------------------
class PadaTable(tables.Table):
    # column
    pada = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
        } 
    })

    sandhi = tables.Column(empty_values=(), verbose_name=_('Sandhi'))

    origin = tables.Column(empty_values=(), verbose_name=_('Origin'))

    def render_sandhi(self, value, record):
        pada = Pada.objects.get(pk=record.pk)
        if pada.get_children().exists():
            children = pada.get_children()
            return ' - '.join(str(child) for child in children) 
        return ''

    def render_origin(self, value, record):
        pada = Pada.objects.get(pk=record.pk)
        if pada.parent:
            descendants = pada.parent.get_descendants(include_self=False)
            return pada.parent.pada + ': ' + ' - '.join(str(descendant) for descendant in descendants) 
        return ''

    # button action
    split_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Sandhi'))

    duplicate_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Dupl.'))

    declension_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Decl.'))

    delete_action = tables.TemplateColumn(
        """
        {% if not record.get_children %}
            <form action="{% url 'pada_delete' padanukkama_id=record.padanukkama.id pk=record.id %}" method="post">
            {% csrf_token %}
            <button
                type="submit"
                onclick="return confirm(\'{{ deleted_conf_message }}\')"
                class="w3-button w3-round-xlarge w3-hover-red">
                <i class="far fa-trash-alt" style="color:lightgray"></i>
            </button>
            </form>
        {% endif %}
        """,
        verbose_name=_('Delete'),
        orderable=False
    )

    class Meta:
        model = Pada
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('pada',)
        
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        
        ## Cache the tree Pada for performance ##
        cache_tree_children(data)
    
    def render_split_action(self, record):
        if record.parent:
            # Record has descendants, do not show split_action
            return ''
        else:
            # Record does not have descendants, show split_action
            url=reverse_lazy('pada_split_sandhi', args=[record.padanukkama_id, record.id])
            return format_html(
                '<a href="{}" class="w3-button w3-round-xlarge w3-hover-brown">'
                '<i class="fas fa-project-diagram" style="color: lightgray"></i></a>',
                url,
            )

    def render_duplicate_action(self, record):
        if record.parent:
            # Record has descendants, do not show duplicate_action
            return ''
        else:
            # Record does not have descendants, show duplicate_action
            message = _('Do you want to duplicate record of ') + record.pada
            url = reverse_lazy('pada_duplicate', args=[record.padanukkama_id, record.id])
            return format_html(
                '<a href="{}" onclick="return confirm(\'{}\')" class="w3-button w3-round-xlarge w3-hover-brown">'
                '<i class="far fa-clone" style="color: lightgray"></i></a>',
                url,
                message
            )

    def render_declension_action(self, record):
        if record.get_descendants().exists():
            # Record has descendants, do not show declension_action
            return ''
        else:
            # Record does not have descendants, show declension_action
            return mark_safe(
                '<a href="{url}" class="w3-button w3-round-xlarge w3-hover-brown"><i class="fas fa-layer-group" style="color: lightgray"></i></a>'.format(
                url=reverse_lazy('pada_split_sandhi', args=[record.padanukkama_id, record.id])
            ))


class PadaFilter(FilterSet):
    class Meta:
        model = Pada
        fields = {"pada": ["startswith", "contains"],}


# -----------------------------------------------------
# PadaParentChildTable
# -----------------------------------------------------
class PadaParentChildTable(tables.Table):
    pada = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
    }})

    declension_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Decl.'))

    delete_action = tables.TemplateColumn(
        """
        {% if record.parent %}
            <form action="{% url 'pada_delete' padanukkama_id=pada.padanukkama.id pk=record.id %}" method="post">
            {% csrf_token %}
            <button
                type="submit"
                onclick="return confirm(\'{{ message }}\')"
                class="w3-button w3-round-xlarge w3-hover-red">
                <i class="far fa-trash-alt" style="color:lightgray"></i>
            </button>
            </form>
        {% endif %}
        """,
        verbose_name='Delete',
        orderable=False
    )

    def render_declension_action(self, record):
        if record.get_descendants().exists():
            # Record has descendants, do not show declension_action
            return ''
        else:
            # Record does not have descendants, show declension_action
            return mark_safe(
                '<a href="{url}" class="w3-button w3-round-xlarge w3-hover-brown"><i class="fas fa-layer-group" style="color: lightgray"></i></a>'.format(
                url=reverse_lazy('pada_split_sandhi', args=[record.padanukkama_id, record.id])
            ))


    class Meta:
        model = Pada
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('pada',)

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        
        ## Cache the tree Pada for performance ##
        cache_tree_children(data)

