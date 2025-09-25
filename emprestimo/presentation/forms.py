from django import forms

from emprestimo.models import TipoOcorrencia


class TipoOcorrenciaForm(forms.ModelForm):
    class Meta:
        model = TipoOcorrencia
        fields = ["descricao"]
