from django import forms

from emprestimo.models import Emprestimo, TipoOcorrencia


class TipoOcorrenciaForm(forms.ModelForm):
    class Meta:
        model = TipoOcorrencia
        fields = ["descricao"]


class CriarEmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = [
            "aluno",
            "bem",
            "observacoes",
            "data_emprestimo",
            "data_devolucao_prevista",
        ]
