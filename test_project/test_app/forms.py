from django import forms

from .models import Data


class TestNameForm(forms.Form):
    name = forms.CharField(max_length=255)


class TestDataForm(forms.ModelForm):

    class Meta:
        model = Data
        fields = ['name']
