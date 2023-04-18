import django_tables2 as tables
from django_filters import FilterSet
from django.utils.translation import gettext_lazy as _

from .models import Word

class WordlistTable(tables.Table):
    word_seq = tables.Column(order_by=("word_seq"), visible=False)
    action = tables.TemplateColumn(
        "<a href='{{ record.id }}' class='w3-button'><i class='fa-solid fa-magnifying-glass'></i></a>"
        )
    
    class Meta:
        model = Word
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("word", "burmese", "book", "page_number",)
        order_by = ("word_seq",)


class WordlistFilter(FilterSet):
    class Meta:
        model = Word
        fields = {"word": ["startswith", "contains"],}