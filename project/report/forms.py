from django.forms import forms

class FileImportForm(forms.Form):
    file = forms.FileField()
