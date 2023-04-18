import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .models import Page

class PagelistTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='digital-archive/{{ record.id }}?{{ request.GET.urlencode }}' class='w3-button'><i class='fa-solid fa-magnifying-glass'></i></a>"
        )
    
    class Meta:
        model = Page
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("page_number", "sample_content", "proofread",)
        order_by = ("page_number",)
