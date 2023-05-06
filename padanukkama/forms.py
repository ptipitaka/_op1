from django import forms

from .models import NamaSaddamala, AkhyataSaddamala


class NamaSaddamalaForm(forms.ModelForm):
    class Meta:
        model = NamaSaddamala
        exclude = ['title_order']


class AkhyataSaddamalaForm(forms.ModelForm):
    class Meta:
        model = AkhyataSaddamala
        exclude = ['title_order']