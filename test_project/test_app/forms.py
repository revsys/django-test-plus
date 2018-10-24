from django import forms

from .models import Data


class NameForm(forms.Form):
    name = forms.CharField(max_length=255)


class DataForm(forms.ModelForm):

    class Meta:
        model = Data
        fields = ['name']
