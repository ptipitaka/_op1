from django import forms
from .models import Edition, Page

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
