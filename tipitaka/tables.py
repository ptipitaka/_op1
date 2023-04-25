import django_tables2 as tables
from django_filters import FilterSet
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mptt.templatetags.mptt_tags import cache_tree_children

from .models import Page, TableOfContent, Structure

class DigitalArchiveTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='digital-archive/{{ record.id }}?{{ request.GET.urlencode }}' class='w3-button'><i class='fa-solid fa-magnifying-glass'></i></a>"
        )
    
    class Meta:
        model = Page
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("page_number", "sample_content",)
        order_by = ("page_number",)


class TocTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='toc/{{ record.slug }}?{{ request.GET.urlencode }}' class='w3-button'><i class='fa-solid fa-magnifying-glass'></i></a>"
        )
    
    class Meta:
        model = TableOfContent
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("code", "edition",)
        order_by = ("code",)


class StructureTable(tables.Table):
    title = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
        } 
    })

    class Meta:
        model = Structure
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('code', 'title', 'breadcrumb',)
        
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        
        # Cache the tree structure for performance
        cache_tree_children(data)

        # Add tree structure to table
        new_data = []
        for row in data:
            new_data.append(row)
            children = row.get_children()
            for child in children:
                child.level = row.level + 1
                # child.parent = row
                new_data.append(child)
        self.data = Structure.objects.filter(pk__in=[obj.pk for obj in new_data])
     

class StructureFilter(FilterSet):
    class Meta:
        model = Structure
        fields = {
            "code": ["contains"],
            "title": ["contains"],
            }

