from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import Edition, Page, WordlistVersion, WordList, Structure, CommonReference

# query form (digital archive page)
class QForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["edition", "volume",]

# page edit form (digital archive page)
class EditForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ("content",)

        widgets = {
            'content': forms.Textarea(attrs={'class': 'w3-input w3-border w3-round'}),
        }

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

    def __init__(self, *args, **kwargs):
        self.structure_id = kwargs.pop('structure_id', None)
        super().__init__(*args, **kwargs)
        
        if self.structure_id:
            # get record from database (Structure)
            structure = get_object_or_404(Structure, id=self.structure_id)
            # ----------------------------------------------------------------
            # finding editions related to this structure
            # ----------------------------------------------------------------
            # 1. get all related wordlist_versions of this structure
            all_related_wordlist_versions = structure.table_of_content.wordlist_version.all()
            # 2. get all related wordlist_versions that are used in common reference
            # 2.1 get all commaon_reference of this structure
            common_refs = CommonReference.objects.filter(structure=structure)
            # 2.2 get all wordlist_version that already added to common reference of this structure
            all_added_wordlist_versions = WordlistVersion.objects.filter(commonreference__in=common_refs)
            # 3. get all wordlist_version that not in common reference
            remain_wordlist_version = all_related_wordlist_versions.exclude(pk__in=all_added_wordlist_versions.values_list('pk', flat=True))
            # 4. get all related Editions of these remain wordlist_versions
            all_related_editions = Edition.objects.filter(wordlistversion__in=remain_wordlist_version)
            # 5. initial fields of this form
            self.fields['edition'].queryset = all_related_editions
            # self.fields['wordlist_version'].queryset = remain_wordlist_version
            # get all wordlist_versions that are already selected
            selected_wordlist_versions = WordList.objects.filter(
                edition__in=all_related_editions
            ).values_list('wordlist_version', flat=True).distinct()
            
            # filter out the selected wordlist_versions from the queryset
            remaining_wordlist_versions = remain_wordlist_version.exclude(
                pk__in=selected_wordlist_versions
            )
            
            # update the queryset of the wordlist_version field
            self.fields['wordlist_version'].queryset = remaining_wordlist_versions
            

    class Meta:
        model = WordList
        fields = ['edition', 'wordlist_version', 'volume', 'page', 'line_number']
        widgets = {
            'line_number': forms.NumberInput(attrs={'step': '1', 'min': '0'}),
            'wordlist_version': forms.Select(attrs={'id': 'wordlist-version-select'}),
        }
