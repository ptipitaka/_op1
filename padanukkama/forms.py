from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeMultipleChoiceField


from .models import NamaSaddamala, AkhyataSaddamala, Padanukkama, Pada, Language, Sadda
from tipitaka.models import WordlistVersion, TableOfContent, Structure

# -----------------------------------------------------
# NamaSaddamalaForm
# -----------------------------------------------------
class NamaSaddamalaForm(forms.ModelForm):
    class Meta:
        model = NamaSaddamala
        exclude = ['title_order']


# -----------------------------------------------------
# AkhyataSaddamalaForm
# -----------------------------------------------------
class AkhyataSaddamalaForm(forms.ModelForm):
    class Meta:
        model = AkhyataSaddamala
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
# PadaForm
# -----------------------------------------------------
class PadaForm(forms.Form):
    namasaddamala = NamaSaddamala.objects.all().order_by('-statistic', 'title_order')
    akhyatasaddamala = AkhyataSaddamala.objects.all().order_by('-statistic', 'title_order')

    # Create a list to store the template data
    template = []

    # initial value
    template.append({
        'unique_id': '',
        'from_table': '',
        'id': '',
        'title': '-----',
        'order': ''
    })

    # Process namasaddamala objects
    for namasaddamala_obj in namasaddamala:
        unique_id = "namasaddamala_" + str(namasaddamala_obj.id)
        order = str(namasaddamala_obj.statistic).zfill(5) + namasaddamala_obj.title_order
        title = namasaddamala_obj.title
        nama_type = namasaddamala_obj.nama_type.title if namasaddamala_obj.nama_type else '-'
        linga = namasaddamala_obj.linga.title if namasaddamala_obj.linga else '-'
        template.append({
            'unique_id': unique_id,
            'from_table': 'namasaddamala',
            'id': namasaddamala_obj.id,
            'title': title + ' (' + nama_type + ', ' + linga + ')',
            'order': order
        })

    # Process akhyatasaddamala objects
    for akhyatasaddamala_obj in akhyatasaddamala:
        unique_id = "akhyatasaddamala_" + str(akhyatasaddamala_obj.id)
        order = str(akhyatasaddamala_obj.statistic).zfill(5) + akhyatasaddamala_obj.title_order
        title = akhyatasaddamala_obj.title
        dhatu = akhyatasaddamala_obj.dhatu.title if akhyatasaddamala_obj.dhatu else '-'
        paccaya = akhyatasaddamala_obj.paccaya.title if akhyatasaddamala_obj.paccaya else '-'
        template.append({
            'unique_id': unique_id,
            'from_table': 'akhyatasaddamala',
            'id': akhyatasaddamala_obj.id,
            'title': title + ' (' + dhatu + ', ' + paccaya + ')',
            'order': order
        })

    # Sort the template by order (statistic and title_order)
    template.sort(key=lambda x: x['order'])

    # Create the selection template for the ChoiceField
    selection_template = [(entry['unique_id'], entry['title']) for entry in template]

    sadda = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'onchange': 'crate_vipatti()'})
    )
    template_selection = forms.ChoiceField(
        choices=selection_template,
        widget=forms.Select(attrs={'onchange': 'crate_vipatti()'})
    )



# -----------------------------------------------------
# SaddaForm
# -----------------------------------------------------
class SaddaForm(forms.ModelForm):
    class Meta:
        model = Sadda
        fields = ['sadda']