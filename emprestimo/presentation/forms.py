from django import forms
from django.forms.widgets import DateInput

from emprestimo.models import Emprestimo, TipoOcorrencia


class TipoOcorrenciaForm(forms.ModelForm):
    class Meta:
        model = TipoOcorrencia
        fields = ["descricao"]


class CriarEmprestimoForm(forms.ModelForm):
    data_emprestimo = forms.DateField(
        label="Data de retirada",
        widget=DateInput(attrs={"type": "date"}),
    )
    data_devolucao_prevista = forms.DateField(
        label="Data de devolução prevista",
        widget=DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = Emprestimo
        fields = [
            "aluno",
            "bem",
            "data_emprestimo",
            "data_devolucao_prevista",
            "observacoes",
        ]
