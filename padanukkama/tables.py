import django_tables2 as tables
from django_filters import FilterSet
from django_tables2.utils import A
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import NamaSaddamala

class NamaSaddamalaTable(tables.Table):

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
        fields = ("title", "linga",)
        order_by = ("title_order",)


class NamaSaddamalaFilter(FilterSet):
    class Meta:
        model = NamaSaddamala
        fields = ("title", "linga", "karanta",)