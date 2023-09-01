import django_tables2 as tables
import django_filters
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django_filters import FilterSet, filters
from django_tables2.utils import A
from mptt.templatetags.mptt_tags import cache_tree_children

from .models import Page, TableOfContent, Structure, WordList, CommonReference

# DigitalArchiveTable
# -------------------
class DigitalArchiveTable(tables.Table):
    action = tables.LinkColumn(
        viewname='digital_archive',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=mark_safe('<i class="fas fa-pencil-alt"></i>'),
        empty_values=(),
        verbose_name=_("Action")
    )
    
    sample_content = tables.Column(
        attrs={"td": {"style": "width: 50%;"}},
        verbose_name=_("Content")
    )

    class Meta:
        model = Page
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("volume", "page_number", "sample_content",)
        order_by = ("page_number",)



# WordlistMasterTable
# -------------------
class WordlistMasterTable(tables.Table):
    word_seq = tables.Column(order_by=("word_seq"), visible=False)
    action = tables.LinkColumn(
        viewname='wordlist_page_source',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=mark_safe('<i class="fas fa-pencil-alt"></i>'),
        empty_values=(),
        verbose_name=_("Action")
    )
    
    class Meta:
        model = WordList
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("code", "word", "word_seq", "word_roman_script", "edition", "wordlist_version",)
        order_by = ("code",)



class WordlistMasterFilter(FilterSet):
    word__startswith = filters.CharFilter(
        field_name='word',
        lookup_expr='startswith',
        label=_('Word starts with'))
    word__contains = filters.CharFilter(
        field_name='word',
        lookup_expr='contains',
        label=_('Word contains'))
    class Meta:
        model = WordList
        fields = {"wordlist_version": ["exact"]}


# TocTable
# --------
class TocTable(tables.Table):    
    action = tables.LinkColumn(
        viewname='structure',
        args=[A('slug')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}},
        text=format_html('<i class="fas fa-pencil-alt"></i>'),
        empty_values=(),
        verbose_name=_("Action")
    )
    class Meta:
        model = TableOfContent
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("code", "wordlist_version",)
        order_by = ("code",)



class StructureTable(tables.Table):
    title = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (30 + (record.level * 30)),
        } 
    })

    def render_title(self, value, record):
        # Customize how the title is displayed along with other fields
        return f"{(record.title_number or '')} {record.title}"


    action = tables.LinkColumn(
        viewname='common_reference_subform',
        args=[A('table_of_content.slug'), A('id')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}},
        text=format_html('<i class="fa-solid fas fa-laptop-code"></i>'),
        empty_values=(),
    )

    class Meta:
        model = Structure
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('code', 'title', 'breadcrumb',)
        
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        
        ## Cache the tree structure for performance ##
        cache_tree_children(data)



class StructureFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="contains",
        label=_("Title contains"),
    )

    deep_search_field = django_filters.ModelChoiceFilter(
        queryset=Structure.objects.filter(level__in=[1, 2, 3]),
        method='search_children',
        label=_("Parent"),
    )

    class Meta:
        model = Structure
        fields = {}

    def __init__(self, *args, **kwargs):
        super(StructureFilter, self).__init__(*args, **kwargs)
        # self.deep_search_field
        self.filters['deep_search_field'].field.label_from_instance = lambda obj: obj.breadcrumb_option


    def search_children(self, queryset, name, value):
        structure = Structure.objects.get(id=value.id)
        descendants = structure.get_descendants(include_self=True)
        return descendants



# WordListTable
# -------------
class WordListTable(tables.Table):
    action = tables.TemplateColumn(
        """
            <div class="w3-bar">
            <button class="w3-bar-item w3-button w3-green" onclick="copyValue('{{ record.code }}', 'T')">
                <i class='fas fa-step-backward' style='font-size:24px'></i>
            </button>
            <button class="w3-bar-item w3-button w3-blue" onclick="copyValue('{{ record.code }}', 'F')">
                <i class='fas fa-step-forward' style='font-size:24px'></i>
            </button>
            </div>
        """
    )
    class Meta:
        model = WordList
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("line_number", "word", "code",)
        order_by = ("code",)



class CommonReferenceTable(tables.Table):
    action = tables.TemplateColumn(
        """
        <a href='/tipitaka/toc/{{ record.structure.table_of_content.slug }}/structure/{{ record.structure.id }}/common-reference/{{ record.id }}' class='w3-button w3-small w3-border w3-round-xlarge w3-hover-brown'>
            <i class='fas fa-glasses'></i>
        </a>
        """
    )

    wlv = tables.Column(accessor="wordlist_version", verbose_name="Wl.V")
    # start = tables.Column(accessor="from_position", verbose_name="Start")
    # end = tables.Column(accessor="to_position", verbose_name="End")
    class Meta:
        model = CommonReference
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("wlv",)
        order_by = ("wordlist_version",)


