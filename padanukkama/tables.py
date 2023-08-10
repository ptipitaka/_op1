import django_filters
import django_tables2 as tables

from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.middleware.csrf import get_token
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet, CharFilter, ChoiceFilter, filters, ModelChoiceFilter
from django_tables2.utils import A
from mptt.templatetags.mptt_tags import cache_tree_children
from simple_history.utils import get_history_manager_for_model

from .models import Padanukkama, Pada, Sadda, LiteralTranslation
from tipitaka.models import Structure

from .workflows import SaddaTranslationWorkflow



# -----------------------------------------------------
# Padanukkama Table & Filter
# -----------------------------------------------------
class PadanukkamaTable(tables.Table):
    title_order = tables.Column(visible=False)
    update = tables.LinkColumn(
        viewname='padanukkama_update',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-hover-brown"}}, 
        text=mark_safe('<i class="fas fa-pencil-alt"></i>'),
        empty_values=(),
        orderable=False,
        verbose_name=_("Update")
    )

    pada_list = tables.LinkColumn(
        viewname='padanukkama_pada',
        args=[A('pk')],
        attrs={"a": {"class": "w3-button w3-round-xlarge w3-border w3-hover-brown"}}, 
        text=mark_safe('<i class="far fa-list"></i>'),
        empty_values=(),
        orderable=False,
        verbose_name=_("Pada")
    )

    sadda_list = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name=_('Sadda')
    )

    def render_sadda_list(self, record):
        url = reverse_lazy('sadda')
        url_with_params = f'{url}?padanukkama={record.pk}'
        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-indigo">'
            f'<i class="far fa-list"></i></a>'
        )

    literal_translation_list = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name=_('Literal Translation')
    )

    def render_literal_translation_list(self, record):
        url = reverse_lazy('literal_translation')
        url_with_params = f'{url}?padanukkama={record.pk}'
        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-orange">'
            f'<i class="far fa-list"></i></a>'
        )


    about = tables.Column(attrs={'td': {'style': 'width: 40%;'}})

    def __init__(self, *args, **kwargs):
        # Get the padanukkama_pk parameter from kwargs
        self.padanukkama_pk = kwargs.pop('padanukkama_pk', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Padanukkama
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("title", "about",)
        order_by = ("title",)
    
class PadanukkamaFilter(FilterSet):
    title__contains = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=_('Title contains'))
    publication = django_filters.BooleanFilter(
        label=_("Publication"),
        widget=forms.Select(
            choices=[(None, _("All")), (True, _("True")), (False, _("False"))]
        )
    )
    class Meta:
        model = Padanukkama
        fields = {}



# -----------------------------------------------------
# Pada Table & Filter
# -----------------------------------------------------
class PadaTable(tables.Table):
    class Meta:
        model = Pada
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('pada',)
        per_page = 10

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        # Cache the tree Pada for performance ##
        cache_tree_children(data)


    # ---------------------- #
    # column / button action #
    # ---------------------- #
    pada = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
        } 
    })
 
    # split action btn
    # -----------------------
    split_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Sandhi'))
    def render_split_action(self, record):
        if record.parent or record.sadda:
            # Record has descendants, do not show split_action
            return ''
        else:
            # Get all the query parameters from the request's GET parameters
            query_params = self.request.GET

            # Generate the URL with the updated parameters
            url = reverse_lazy('pada_split_sandhi', args=[record.padanukkama_id, record.id])
            url_with_params = f'{url}?{query_params.urlencode()}'
            
            return mark_safe(
                f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
                f'<i class="fas fa-project-diagram w3-text-orange"></i></a>'
            )
        
    # sandhi
    # ------
    sandhi = tables.Column(empty_values=(), verbose_name=_('Sandhi'))
    def render_sandhi(self, value, record):
        pada = Pada.objects.get(pk=record.pk)
        if pada.get_children().exists():
            children = pada.get_children()
            return ' - '.join(str(child) for child in children) 
        return ''
    
    # origin
    # ------
    origin = tables.Column(empty_values=(), verbose_name=_('Origin'))
    def render_origin(self, value, record):
        pada = Pada.objects.get(pk=record.pk)
        if pada.parent:
            descendants = pada.parent.get_descendants(include_self=False)
            return pada.parent.pada + ': ' + ' - '.join(str(descendant) for descendant in descendants) 
        return ''
    
    # declension action btn
    # ---------------------
    sadda_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Sadda'))
    def render_sadda_action(self, record):
        if record.get_descendants().exists():
            # Record has descendants, do not show sadda_action
            return ''
        else:
            # Get all the query parameters from the request's GET parameters
            query_params = self.request.GET

            # Generate the URL with the updated parameters
            url = reverse_lazy('pada_declension', args=[record.padanukkama_id, record.id])
            url_with_params = f'{url}?{query_params.urlencode()}'

            return mark_safe(
                f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
                f'<i class="fas fa-layer-group w3-text-indigo"></i></a>'
            )

    # sadda
    # -----
    sadda = tables.Column(empty_values=(), verbose_name=_('Sadda'))
    def render_sadda(self, value, record):
        pada = Pada.objects.get(pk=record.pk)
        if pada.sadda:
            return pada.sadda.sadda
        return ''
    
    # duplication action btn
    # ----------------------
    duplicate_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Dupl.'))
    def render_duplicate_action(self, record):
        if record.parent:
            # Record has descendants, do not show duplicate_action
            return ''
        else:
            # Get all the query parameters from the request's GET parameters
            query_params = self.request.GET

            # Generate the URL with the updated parameters
            message = _('Do you want to duplicate record of ') + record.pada
            url = reverse_lazy('pada_duplicate', args=[record.padanukkama_id, record.id])
            url_with_params = f'{url}?{query_params.urlencode()}'
            return mark_safe(
                f'<a href="{ url_with_params }" onclick="return confirm(\'{ message }\')" class="w3-button w3-round-xlarge w3-hover-white">'
                f'<i class="far fa-clone w3-text-teal"></i></a>'
            )

    # delete action btn
    # -----------------
    delete_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Delete'))
    def render_delete_action(self, record):
        if record.get_children():
            # Record has descendants, do not show delete_action
            return ''
        else:
            # Get all the query parameters from the request's GET parameters
            query_params = self.request.GET

            # Generate the URL with the updated parameters
            message = _('Do you want to delete record of ') + record.pada
            url = reverse_lazy('pada_delete', args=[record.padanukkama_id, record.id])
            url_with_params = f'{url}?{query_params.urlencode()}'
            return mark_safe(
                f'<a href="{ url_with_params }" onclick="return confirm(\'{ message }\')" class="w3-button w3-round-xlarge w3-hover-white">'
                f'<i class="far fa-trash-alt w3-text-red"></i></a>'
            )


class PadaFilter(FilterSet):
    OPTION_CHOICES = [
        ('SW', _("Search for Padas that start with these characters")),
        ('CT', _("Search for Padas that contain these characters")),
        ('IN', _("Go to the page where this Pada is located")),
        ('LP', _("Go to the page of the latest updated Pada")),
    ]
    PAGINATE_BY=10
    page_number=None

    pada_filter = CharFilter(
        label=_('Pada'),
        method="filter_pada_with_options"
    )

    pada_filter_options = ChoiceFilter(
        label=_("Please select"),
        choices=OPTION_CHOICES,
        method="filter_pada_with_options"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['pada_filter_options'].initial = 'SW'

    def filter_pada_with_options(self, queryset, name, value):
        if value:
            pada_value = self.form.cleaned_data['pada_filter']
            if value == "SW":
                return queryset.filter(pada__startswith=pada_value)
            elif value == "CT":
                return queryset.filter(pada__contains=pada_value)
            elif value == 'IN':
                self.page_number = self.get_page_number_containing_keyword(queryset, pada_value)
                return queryset
            elif value == 'LP':
                history_manager = get_history_manager_for_model(Sadda)
                try:
                    last_sadda_updated = history_manager.filter(
                        history_user=self.request.user).latest('history_date')
                    sadda=Sadda.objects.filter(sadda=last_sadda_updated.sadda).first()
                    if sadda:
                        pada_value = Pada.objects.get(sadda=sadda.id)
                        if pada_value:
                            self.page_number = self.get_page_number_containing_keyword(queryset, pada_value.pada)
                except:
                    self.page_number = None
                return queryset
            else:
                return queryset

    def get_page_number_containing_keyword(self, queryset, pada_value):
        paginator = Paginator(queryset, self.PAGINATE_BY)
        for page_number in paginator.page_range:
            page = paginator.page(page_number)
            if any(pada_value in item.pada for item in page.object_list):
                return page_number
        return None

    class Meta:
        model = Pada
        fields = {}



# -----------------------------------------------------
# PadaParentChildTable
# -----------------------------------------------------
class PadaParentChildTable(tables.Table):
    pada = tables.Column(attrs={'td': {
        'style': lambda value, record: 'padding-left: %spx' % (50 + (record.level * 50)),
    }})

    sadda_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Decl.'))
    def render_sadda_action(self, record):
        if record.get_descendants().exists():
            # Record has descendants, do not show sadda_action
            return ''
        else:
            # Get all the query parameters from the request's GET parameters
            query_params = self.request.GET

            # Generate the URL with the updated parameters
            url = reverse_lazy('pada_declension', args=[record.padanukkama_id, record.id])
            url_with_params = f'{url}?{query_params.urlencode()}'
            return mark_safe(
                f'<a href="{ url_with_params }" class="w3-button w3-round-xlarge w3-hover-white">'
                f'<i class="fas fa-layer-group w3-text-indigo"></i></a>'
            )
        
    delete_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Delete'))
    def render_delete_action(self, record):
        if not record.parent:
            # Record has descendants, do not show delete_action
            return ''
        else:
            # Get all the query parameters from the request's GET parameters
            query_params = self.request.GET

            # Generate the URL with the updated parameters
            message = _('Do you want to delete record of ') + record.pada
            url = reverse_lazy('pada_delete', args=[record.padanukkama_id, record.id])
            url_with_params = f'{url}?{query_params.urlencode()}'
            return mark_safe(
                f'<a href="{ url_with_params }" onclick="return confirm(\'{ message }\')" class="w3-button w3-round-xlarge w3-hover-white">'
                f'<i class="far fa-trash-alt w3-text-red"></i></a>'
            )

    class Meta:
        model = Pada
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('pada',)

    def __init__(self, data, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(data, *args, **kwargs)
        
        ## Cache the tree Pada for performance ##
        cache_tree_children(data)



# -----------------------------------------------------
# TranslatePadaParentChildTable
# -----------------------------------------------------
class TranslatePadaParentChildTable(tables.Table):
    pada = tables.Column(attrs={'td': {
        'style': lambda value, record: 'min-width: 200px; padding-left: %spx' % (15 + (record.level * 40)),
    }})

    translate_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Translate Sadda'))
    def render_translate_action(self, record):
        if record.get_descendants().exists():
            # Record has descendants, do not show translate_action
            return ''
        else:
            # Generate the URL with the updated parameters
            url = reverse_lazy('htmx_translation_pada_translate', args=[self.translate_word_id, record.id])

            return mark_safe(
                f'<button hx-get="{url}" hx-target="#htmx-translation-form"'
                f'class="w3-button w3-round-xlarge w3-border w3-hover-white">'
                f'<i class="fas fa-layer-group w3-text-indigo"></i>'
                f'</button>'
            )
        
    delete_action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Delete'))
    def render_delete_action(self, record):
        if not record.parent:
            # Record has descendants, do not show delete_action
            return ''
        else:
            # Generate the URL with the updated parameters
            message = _('Do you want to delete record of ') + record.pada
            url = reverse_lazy('htmx_translation_pada_delete', args=[self.translate_word_id, record.id])

            csrf_token = get_token(self.request)

            return mark_safe(
                f'<form hx-post="{url}" hx-target="#htmx-translation-form" method="post">'
                f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">'
                f'<button type="submit" onclick="return confirm(\'{message}\')" class="w3-button w3-round-xlarge w3-border w3-hover-white">'
                f'<i class="far fa-trash-alt w3-text-red"></i>'
                f'</button>'
                f'</form>'
            )

    class Meta:
        model = Pada
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('pada',)

    def __init__(self, data, *args, **kwargs):
        self.translate_word_id = kwargs.pop('translate_word_id', None)
        super().__init__(data, *args, **kwargs)
        
        ## Cache the tree Pada for performance ##
        cache_tree_children(data)


# -----------------------------------------------------
# Sadda Table & Filter
# -----------------------------------------------------
class SaddaTable(tables.Table):
    sadda_seq = tables.Column(visible=False)
    pada = tables.Column(verbose_name=_('Related Padas'))
    created_by = tables.Column(empty_values=(), orderable=False, verbose_name=_('Created by'))
    action = tables.Column(empty_values=(), orderable=False, verbose_name=_('Action'))

    class Meta:
        model = Sadda
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ("sadda", "construction", "pada", "state", "created_by", "padanukkama")
        order_by = ("sadda_seq",)
        per_page = 10

    def render_pada(self, value, record):
        pada_list = record.pada.all().order_by('pada_seq')
        unique_pada_list = list(set(pada.pada for pada in pada_list))
        return ', '.join(unique_pada_list)

    def render_created_by(self, value, record):
        log_activities = record.history.filter(history_type='+')
        user_list = [f"{activity.history_user} ({activity.history_date.strftime('%d-%b-%Y')})" for activity in log_activities]
        user_string = ', '.join(user_list)
        return user_string

    def render_action(self, record):
        # Get all the query parameters from the request's GET parameters
        query_params = self.request.GET

        # Generate the URL with the updated parameters
        url = reverse_lazy('sadda_update', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'

        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
            f'<i class="fas fa-pencil-alt"></i></a>'
        )

class SaddaFilter(FilterSet):
    PAGINATE_BY=10
    PAGE_NUMBER=None

    padanukkama = ModelChoiceFilter(
        queryset=Padanukkama.objects.none(),  # Set an initial empty queryset
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_("Padanukkama")
    )

    state = ChoiceFilter(
        field_name='state',
        choices=(),
        label=_('State')
    )

    creator = ChoiceFilter(
        label=_("Created By"),
        choices=(),
        method="filter_sadda_with_creator"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # padanukkama
        # -----------
        self.filters['padanukkama'].field.queryset = Padanukkama.objects.filter(
            collaborators__id=self.request.user.id
        )
        # state variables
        # ---------------
        STATUS = [
            (state.name, _(state.name.capitalize()))
            for state in SaddaTranslationWorkflow.states
        ]
        self.filters['state'].extra['choices'] = STATUS
        # creator variable
        # ----------------
        current_user = self.request.user
        # Retrieve all Padanukkama instances where the current user is a collaborator
        participating_padas = Padanukkama.objects.filter(collaborators=current_user)
        # Get all users from the participating Padanukkama instances
        users = User.objects.filter(padanukkama__in=participating_padas).distinct()
        # Convert the users queryset to a list of tuples (value, label)
        USER_CHOICES = [(user.id, user.get_full_name()) for user in users]
        # Assign the choices to the creator filter
        self.filters['creator'].extra['choices'] = USER_CHOICES

    def filter_sadda_with_creator(self, queryset, name, value):
        if value:
            # Filter the queryset by creator
            filtered_saddas = Sadda.history.filter(history_user_id=value, history_type='+').values('id')
            queryset = queryset.filter(id__in=filtered_saddas)
        return queryset


    class Meta:
        model = Sadda
        fields = ("padanukkama", "sadda", "sadda_type", "state",)



# -----------------------------------------------------
# LiteralTranslation Table & Filter
# -----------------------------------------------------
class LiteralTranslationTable(tables.Table):
    update_action = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Update'))
    
    translation_action = tables.Column(
        empty_values=(), orderable=False, verbose_name=_('Translation'))

    class Meta:
        model = LiteralTranslation
        template_name = "django_tables2/w3css.html"
        attrs = {"class": "w3-table w3-bordered"}
        fields = ('padanukkama', 'title', 'wordlist_version')
        order_by = ("title",)
        per_page = 10

    def render_update_action(self, record):
        # Get all the query parameters from the request's GET parameters
        query_params = self.request.GET

        # Generate the URL with the updated parameters
        url = reverse_lazy('literal_translation_update', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'

        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-brown">'
            f'<i class="fas fa-pencil-alt"></i></a>'
        )
    
    def render_translation_action(self, record):
        # Get all the query parameters from the request's GET parameters
        query_params = self.request.GET

        # Generate the URL with the updated parameters
        url = reverse_lazy('literal_translation_translate', args=[record.id])
        url_with_params = f'{url}?{query_params.urlencode()}'

        return mark_safe(
            f'<a href="{url_with_params}" class="w3-button w3-round-xlarge w3-border w3-hover-blue">'
            f'<i class="fa fa-book"></i></a>'
        )


class LiteralTranslationFilter(FilterSet):
    padanukkama = ModelChoiceFilter(
        queryset=Padanukkama.objects.none(),  # Set an initial empty queryset
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_("Padanukkama")
    )
    class Meta:
        model = LiteralTranslation
        fields = ("padanukkama", "title",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # padanukkama
        # -----------
        self.filters['padanukkama'].field.queryset = Padanukkama.objects.filter(
            collaborators__id=self.request.user.id
        )



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
        
        ## Cache the tree structure for performance ##
        cache_tree_children(data)