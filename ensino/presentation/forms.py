from django import forms

from ensino.models import Campus


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ["nome", "sigla"]
