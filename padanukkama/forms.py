from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_select2.forms import *
from mptt.forms import TreeNodeMultipleChoiceField

from .models import NamaSaddamala, Padanukkama, Pada, Language, Sadda, \
                    VerbConjugation, LiteralTranslation, TranslatedWord
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
        output = ['<div class="scrollable-div">']
        id_ = final_attrs.get('id')
        output.append('<div class="checkbox-options">')
        for i, (option_value, option_label) in enumerate(self.choices):
            checkbox_id = f'{id_}_{i}'
            checked = option_value in value
            output.append(
                f'<div><label for="{checkbox_id}">'
                f'<input type="checkbox" class="structure-checkbox-select" name="{name}" value="{option_value}" id="{checkbox_id}"'
                f'{" checked" if checked else ""}>'
                f'{option_label}</label></div>'
            )
        output.append('</div></div>')
        return mark_safe('\n'.join(output))

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = dict(base_attrs, **(extra_attrs or {}))
        return attrs

    def format_value(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]
        return [str(v) for v in value]

    

# -----------------------------------------------------
# PadanukkamaUpdateForm
# -----------------------------------------------------
class StructureTitleOnlyTreeNodeMultipleChoiceField(TreeNodeMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.level * '--'} {obj.title_number or ''} {obj.title}"
    
class PadanukkamaUpdateForm(forms.ModelForm):
    structure = StructureTitleOnlyTreeNodeMultipleChoiceField(
        queryset=Structure.objects.none(),
        widget=CheckboxMultipleSelect(
        attrs={'class': 'structure-checkbox-select'})
    )
    
    wordlist_version = forms.ModelMultipleChoiceField(
        queryset=WordlistVersion.objects.all(),
        widget=CheckboxSelectMultiple(
            attrs={'class': 'checkbox-select'}))

    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple(
            attrs={'class': 'checkbox-select'}))

    target_languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=CheckboxSelectMultiple(
            attrs={'class': 'checkbox-select'}))

    def __init__(self, *args, **kwargs):
        table_of_content = kwargs.pop('table_of_content')
        super().__init__(*args, **kwargs)
        self.fields['table_of_content'].disabled = True
        self.fields['wordlist_version'].queryset = table_of_content.wordlist_version.order_by(
            'edition__code', 'version')
        self.fields['structure'].queryset = Structure.objects.filter(
            table_of_content=table_of_content,
            level__in=[1, 2, 3, 4])

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
# LiteralTranslationCreateForm
# -----------------------------------------------------
class LiteralTranslationCreateForm(forms.ModelForm):
    padanukkama = forms.ModelChoiceField(
        queryset=Padanukkama.objects.all(),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        to_field_name='title')

    def __init__(self, *args, **kwargs):
        padanukkama_instance = kwargs.pop('padanukkama_instance', None)
        super().__init__(*args, **kwargs)

        # Use the 'padanukkama_instance' for any additional processing in the form if needed
        if padanukkama_instance:
            # Set a default value for a field based on 'padanukkama_instance'
            self.fields['padanukkama'].initial = padanukkama_instance
            self.fields['title'].initial = f"Translation for {padanukkama_instance.title}"
            self.fields['wordlist_version'].queryset = padanukkama_instance.wordlist_version.all()

    class Meta:
        model = LiteralTranslation
        exclude = ['publication']



# -----------------------------------------------------
# LiteralTranslationUpdateForm
# -----------------------------------------------------
class LiteralTranslationUpdateForm(forms.ModelForm):

    class Meta:
        model = LiteralTranslation
        exclude = ['padanukkama', 'wordlist_version']



# -----------------------------------------------------
# TranslatedWordForm
# -----------------------------------------------------
class TranslatedWordForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5}),  # Setting rows to 5
        required=False,
        label=_('Description'),
    )

    class Meta:
        model = TranslatedWord
        fields = ['translation', 'description',]



# -----------------------------------------------------
# TranslatedWordAddForm
# -----------------------------------------------------
class TranslatedWordAddForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5}),  # Setting rows to 5
        required=False,
        label=_('Description'),
    )

    class Meta:
        model = TranslatedWord
        fields = ['word', 'translation', 'description',]

# -----------------------------------------------------
# LiteralTranslationSaddaForm
# -----------------------------------------------------
def FilterVerbConjugation(word):
    fields = [
        "p1_para_sg", "p1_para_pl", "p1_atta_sg", "p1_atta_pl",
        "p2_para_sg", "p2_para_pl", "p2_atta_sg", "p2_atta_pl",
        "p3_para_sg", "p3_para_pl", "p3_atta_sg", "p3_atta_pl"
    ]
    
    id_list = []

    verb_conjugations = VerbConjugation.objects.all()
    for verb_conjugation in verb_conjugations:
        endings_lists = [getattr(verb_conjugation, field).split(',') for field in fields]

        for endings_list in endings_lists:
            for ending in endings_list:
                if word.endswith(ending.strip()):
                    id_list.append(verb_conjugation.id)
                    break

    if id_list:
        # return VerbConjugation.objects.filter(id__in=id_list).order_by('sequence')
        matched_verb_conjugations = VerbConjugation.objects.filter(id__in=id_list).order_by('sequence')
        return "𝓲 " + ", ".join([vc.title for vc in matched_verb_conjugations])
    else:
        # return VerbConjugation.objects.all().order_by('sequence')
        return None



class LiteralTranslationSaddaForm(forms.ModelForm):
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

    meaning = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),  # Setting rows to 5
        required=False,
        label=_('Meaning'),
    )

    class Meta:
        model = Sadda
        exclude = ['sadda_seq', 'description', 'padanukkama', 'state']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sadda = self.initial.get('sadda', None)

        if sadda:
            # verb_conjugation_queryset = FilterVerbConjugation(sadda)
            # self.fields['verb_conjugation'].queryset = verb_conjugation_queryset
            help_text_result = FilterVerbConjugation(sadda)
            self.fields['verb_conjugation'].help_text = help_text_result



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

    meaning = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),  # Setting rows to 5
        required=False,
        label=_('Meaning'),
    )
    
    class Meta:
        model = Sadda
        exclude = ['sadda_seq']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sadda = self.initial.get('sadda', None)

        if sadda:
            # verb_conjugation_queryset = FilterVerbConjugation(sadda)
            # self.fields['verb_conjugation'].queryset = verb_conjugation_queryset
            help_text_result = FilterVerbConjugation(sadda)
            self.fields['verb_conjugation'].help_text = help_text_result


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



