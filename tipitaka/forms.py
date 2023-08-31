from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeMultipleChoiceField
from .models import Edition, Page, WordlistVersion, WordList, Structure, CommonReference

# query form (digital archive page)
class DigitalArchiveForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["edition", "volume", "page_number", "content"]
        widgets = {
            'content': forms.TextInput(attrs={'rows': 1, 'max_length': 200, 'required': False})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['volume'].required = False
        self.fields['page_number'].required = False
        self.fields['content'].required = False


# page edit form (digital archive page)
class EditForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ("content",)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w3-input w3-border w3-round'}),
        }


class UpdWlAndPageForm(forms.ModelForm):
    word = forms.CharField(label=_("Word"), required=True, max_length=150)
    content = forms.CharField(label=_("Content"), required=True, widget=forms.Textarea(attrs={'class': 'w3-input w3-border w3-round'}))

    class Meta:
        model = WordList
        fields = ['word']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            try:
                page = instance.page
                self.fields['content'].initial = page.content
            except Page.DoesNotExist:
                pass

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            try:
                page = instance.page
                page.content = self.cleaned_data['content']
                page.save()
            except Page.DoesNotExist:
                pass
        return instance


# wordlist generator form (wordlist generator page)
class WLGForm(forms.Form):
    edition = forms.ModelChoiceField(
        queryset=Edition.objects.filter(digitization=True),
        required=True
        )

class CommonReferenceForm(forms.ModelForm):
    class Meta:
        model = CommonReference
        fields = ['from_position', 'to_position',]
        widgets = {
            'from_position': forms.TextInput(attrs={'class': 'w3-input'}),
            'to_position': forms.TextInput(attrs={'class': 'w3-input'}),
        }


class WordlistFinderForm(forms.ModelForm):
    from_p = forms.CharField(label=_("From Position"), required=False,  max_length=20)
    to_p = forms.CharField(label=_("To Position"), required=False,  max_length=20)

    class Meta:
        model = WordList
        fields = ['edition', 'wordlist_version', 'volume', 'page', 'line_number']
        widgets = {
            'line_number': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
        }
    # ----------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        self.structure_id = kwargs.pop('structure_id', None)
        super().__init__(*args, **kwargs)
        
        if self.structure_id:
            # get record from database (Structure)
            structure = get_object_or_404(Structure, id=self.structure_id)
            # ----------------------------------------------------------------
            # finding editions related to this structure
            # ----------------------------------------------------------------
            # Get all related WordlistVersions of this structure
            all_related_wordlist_versions = structure.table_of_content.wordlist_version.all()

            # Get all related Editions of these WordlistVersions
            all_related_editions = Edition.objects.filter(wordlistversion__in=all_related_wordlist_versions)

            # Get unique Editions based on code field
            self.fields['edition'].queryset = all_related_editions.distinct('code')




