from django import forms

from patrimonio.models import TipoBem


class TipoBemForm(forms.ModelForm):
    class Meta:
        model = TipoBem
        fields = ["descricao"]
