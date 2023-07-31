from django import forms

from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from django_select2.forms import *

from padanukkama.models import NamaSaddamala, Dhatu, Paccaya, \
                    AkhyataSaddamala, VerbConjugation



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
# NamaSaddamalaForm
# -----------------------------------------------------
class NamaSaddamalaForm(forms.ModelForm):
    class Meta:
        model = NamaSaddamala
        exclude = ['title_order']



# -----------------------------------------------------
# DhatuForm
# -----------------------------------------------------
class DhatuForm(forms.ModelForm):
    paccaya = forms.ModelMultipleChoiceField(
        queryset=Paccaya.objects.all(),
        widget=CheckboxMultipleSelect(
            attrs={'class': 'structure-checkbox-select'}
        )
    )

    class Meta:
        model = Dhatu
        exclude = ['title_order', 'popularity']



# -----------------------------------------------------
# VerbConjugationForm
# -----------------------------------------------------
class VerbConjugationForm(forms.ModelForm):
    class Meta:
        model = VerbConjugation
        fields = '__all__'




# -----------------------------------------------------
# AkhyataSaddamalaForm
# -----------------------------------------------------
class AkhyataSaddamalaForm(forms.ModelForm):
    class Meta:
        model = AkhyataSaddamala
        exclude = ['title_order']