from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_select2.forms import *
from mptt.forms import TreeNodeMultipleChoiceField

from .models import NamaSaddamala, Padanukkama, Pada, Language, Sadda, VerbConjugation
from tipitaka.models import WordlistVersion, Structure


# -----------------------------------------------------
# NamaSaddamalaForm
# -----------------------------------------------------
class NamaSaddamalaForm(forms.ModelForm):
    class Meta:
        model = NamaSaddamala
        exclude = ['title_order']



# -----------------------------------------------------
# PadanukkamaCreateForm
# -----------------------------------------------------
class PadanukkamaCreateForm(forms.ModelForm):
    class Meta:
        model = Padanukkama
        exclude = ['structure', 'wordlist_version']


# -----------------------------------------------------
# CheckboxMultipleSelect
# -----------------------------------------------------
class CheckboxMultipleSelect(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(self.attrs, attrs)
        output = []
        id_ = final_attrs.get('id')
        for i, (option_value, option_label) in enumerate(self.choices):
            checkbox_id = f'{id_}_{i}'
            checked = option_value in value
            output.append(
                f'<div><label for="{checkbox_id}">'
                f'<input type="checkbox" class="structure-checkbox-select" name="{name}" value="{option_value}" id="{checkbox_id}"'
                f'{" checked" if checked else ""}>'
                f'{option_label}</label></div>'
            )
        return mark_safe('\n'.join(output))
    

# -----------------------------------------------------
# PadanukkamaUpdateForm
# -----------------------------------------------------
class PadanukkamaUpdateForm(forms.ModelForm):
    structure = TreeNodeMultipleChoiceField(
        queryset=Structure.objects.none(),
        widget=CheckboxMultipleSelect(
        attrs={'class': 'structure-checkbox-select'})
    )
    
    wordlist_version = forms.ModelMultipleChoiceField(
        queryset=WordlistVersion.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select'}))

    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select'}))

    target_languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select'}))

    def __init__(self, *args, **kwargs):
        table_of_content = kwargs.pop('table_of_content')
        super().__init__(*args, **kwargs)
        self.fields['table_of_content'].disabled = True
        self.fields['wordlist_version'].queryset = table_of_content.wordlist_version.order_by(
            'edition__code', 'version')
        self.fields['structure'].queryset = Structure.objects.filter(
            table_of_content=table_of_content,
            level__in=[1, 2])

    class Meta:
        model = Padanukkama
        fields = '__all__'


# -----------------------------------------------------
# AddChildPadaForm
# -----------------------------------------------------
class AddChildPadaForm(forms.ModelForm):
    class Meta:
        model = Pada
        fields = ['pada',]



# -----------------------------------------------------
# SaddaForm
# -----------------------------------------------------
class SaddaForm(forms.ModelForm):
    padanukkama = forms.ModelChoiceField(
        queryset=Padanukkama.objects.all(),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        to_field_name='title')

    namasaddamala = forms.ModelMultipleChoiceField(
        queryset=NamaSaddamala.objects.all().order_by('-popularity', 'linga', 'title_order'),
        widget=Select2MultipleWidget,
        required=False,
        label=_('NamaSaddamala')
    )

    verb_conjugation = forms.ModelMultipleChoiceField(
        queryset=VerbConjugation.objects.all().order_by('sequence'),
        widget=Select2MultipleWidget,
        required=False,
        label=_('Verb Conjugation')
    )


    class Meta:
        model = Sadda
        exclude = ['sadda_seq']



# -----------------------------------------------------
# ExportSaddaForm
# -----------------------------------------------------
FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json')
)

class ExportSaddaForm(forms.Form):
    format = forms.ChoiceField(
        choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'w3-select'}),
        required=True,
        label=_('Format')
    )
