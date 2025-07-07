from django import forms

from patrimonio.models import EstadoConservacao, GrauFragilidade, TipoBem


class TipoBemForm(forms.ModelForm):
    class Meta:
        model = TipoBem
        fields = ["descricao"]


class EstadoConservacaoForm(forms.ModelForm):
    class Meta:
        model = EstadoConservacao
        fields = ["nivel", "descricao"]


class GrauFragilidadeForm(forms.ModelForm):
    class Meta:
        model = GrauFragilidade
        fields = ["nivel", "descricao"]
