from django import forms

from patrimonio.models import EstadoConservacao, TipoBem


class TipoBemForm(forms.ModelForm):
    class Meta:
        model = TipoBem
        fields = ["descricao"]


class EstadoConservacaoForm(forms.ModelForm):
    class Meta:
        model = EstadoConservacao
        fields = ["nivel", "descricao"]
