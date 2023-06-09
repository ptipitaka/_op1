import django_tables2 as tables
from django_filters import FilterSet, filters
from django_tables2.utils import A
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Word

class WordlistTable(tables.Table):
    word_seq = tables.Column(order_by=("word_seq"), visible=False)
    action = tables.LinkColumn(
        viewname='abidan_details',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=mark_safe('<i class="fa-solid fa-magnifying-glass"></i>'),
        empty_values=(),
        verbose_name=_('Action')
    )

    class Meta:
        model = Word
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("word", "burmese", "book", "page_number",)
        order_by = ("word_seq",)


class WordlistFilter(FilterSet):
    word__startswith = filters.CharFilter(
        field_name='word',
        lookup_expr='startswith',
        label=_('Word starts with'))
    word__contains = filters.CharFilter(
        field_name='word',
        lookup_expr='contains',
        label=_('Word contains'))

    class Meta:
        model = Word
        fields = {"word": ["startswith", "contains"],}
