from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeMultipleChoiceField

from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama, Pada, Language
from tipitaka.models import WordlistVersion, TableOfContent, Structure


class NamaSaddamalaForm(forms.ModelForm):
    class Meta:
        model = NamaSaddamala
        exclude = ['title_order']


class AkhyataSaddamalaForm(forms.ModelForm):
    class Meta:
        model = AkhyataSaddamala
        exclude = ['title_order']


class PadanukkamaCreateForm(forms.ModelForm):
    class Meta:
        model = Padanukkama
        exclude = ['structure', 'wordlist_version']


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

