import django_tables2 as tables
import django_filters
from django_filters import FilterSet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.templatetags.mptt_tags import cache_tree_children

from .models import Page, TableOfContent, Structure, WordList, CommonReference

class DigitalArchiveTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='/inscriber/digital-archive/{{ record.id }}?{{ request.GET.urlencode }}' class='w3-button'><i class='fa-solid fa-magnifying-glass'></i></a>"
        )
    
    class Meta:
        model = Page
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("page_number", "sample_content",)
        order_by = ("page_number",)


class TocTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='/inscriber/toc/{{ record.slug }}/structure/' class='w3-button'><i class='fa-solid fa-magnifying-glass'></i></a>"
        )
    
    class Meta:
        model = TableOfContent
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("code", "wordlist_version",)
        order_by = ("code",)


class StructureTable(tables.Table):
    title = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
        } 
    })
    action = tables.TemplateColumn(
        "<a href='/inscriber/toc/{{ record.table_of_content.slug }}/structure/{{ record.id }}/common-reference' class='w3-button'><i class='fa-solid fas fa-laptop-code'></i></a>"
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

        ## Add tree structure to table ##
        # new_data = []
        # for row in data:
        #     new_data.append(row)
        #     children = row.get_children()
        #     for child in children:
        #         child.level = row.level + 1
        #         new_data.append(child)
        # self.data = Structure.objects.filter(pk__in=[obj.pk for obj in new_data])

class StructureFilter(FilterSet):    
    deep_search_field = django_filters.ModelChoiceFilter(
        queryset=Structure.objects.filter(level__in=[1, 2, 3]),
        method='search_children',
        label=_("Parent"),
    )

    class Meta:
        model = Structure
        fields = {"title": ["contains"],}

    def __init__(self, *args, **kwargs):
        super(StructureFilter, self).__init__(*args, **kwargs)
        # self.deep_search_field
        self.filters['deep_search_field'].field.label_from_instance = lambda obj: obj.breadcrumb_option


    def search_children(self, queryset, name, value):
        structure = Structure.objects.get(id=value.id)
        descendants = structure.get_descendants(include_self=True)
        return descendants


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
        <a href='/inscriber/toc/{{ record.structure.table_of_content.slug }}/structure/{{ record.structure.id }}/common-reference/{{ record.id }}' class='w3-button'>
            <i class='fas fa-glasses'></i>
        </a>
        """
    )

    wlv = tables.Column(accessor="wordlist_version", verbose_name="Wl.V")
    start = tables.Column(accessor="from_position", verbose_name="Start")
    end = tables.Column(accessor="to_position", verbose_name="End")
    class Meta:
        model = CommonReference
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("wlv", "start", "end",)
        order_by = ("wordlist_version",)


