from django import forms


class TestNameForm(forms.Form):
    name = forms.CharField(max_length=255)
