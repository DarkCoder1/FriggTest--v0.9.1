from django import forms

class FriggForm(forms.Form):
    question = forms.CharField(
        label='digite uma pergunta',
        max_length=55
    )

class UploadForm(forms.Form):
    file = forms.FileField(
        label="Escolha um arquivo",
        help_text="Max. 256kb"
    )