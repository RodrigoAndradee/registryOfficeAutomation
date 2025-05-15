from django import forms

class UploadJSONForm(forms.Form):
    file = forms.FileField(
        label='Selecione um arquivo JSON',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'id': 'inputGroupFile02',
        })
    )
