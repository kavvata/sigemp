from django import forms

from patrimonio.models import (
    Bem,
    EstadoConservacao,
    GrauFragilidade,
    MarcaModelo,
    TipoBem,
)


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


class MarcaModeloForm(forms.ModelForm):
    class Meta:
        model = MarcaModelo
        fields = ["marca", "modelo"]


class BemForm(forms.ModelForm):
    class Meta:
        model = Bem
        fields = [
            "patrimonio",
            "descricao",
            "tipo",
            "grau_fragilidade",
            "estado_conservacao",
            "marca_modelo",
        ]
