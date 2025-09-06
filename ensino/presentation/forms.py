from django import forms
from django.forms.widgets import DateInput

from ensino.models import Aluno, Campus, Curso, FormaSelecao


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ["nome", "sigla"]


class CursoForm(forms.ModelForm):
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.filter(removido_em__isnull=True)
    )

    class Meta:
        model = Curso
        fields = ["nome", "sigla", "campus"]


class FormaSelecaoForm(forms.ModelForm):
    periodo_inicio = forms.DateField(
        label="Início da forma de seleção",
        widget=DateInput(attrs={"type": "date"}),
    )
    periodo_fim = forms.DateField(
        label="Fim da forma de seleção",
        widget=DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = FormaSelecao
        fields = [
            "descricao",
            "periodo_inicio",
            "periodo_fim",
        ]

    def clean_periodo_fim(self):
        periodo_inicio = self.cleaned_data["periodo_inicio"]
        periodo_fim = self.cleaned_data["periodo_fim"]

        if periodo_inicio > periodo_fim:
            raise forms.ValidationError(
                "Data de início não pode ser maior que a data final."
            )

        return periodo_fim


class AlunoForm(forms.ModelForm):
    nome_responsavel = forms.CharField(required=False)
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.filter(removido_em__isnull=True)
    )

    forma_selecao = forms.ModelChoiceField(
        queryset=FormaSelecao.objects.filter(removido_em__isnull=True)
    )

    class Meta:
        model = Aluno
        fields = [
            "nome",
            "nome_responsavel",
            "cpf",
            "email",
            "matricula",
            "telefone",
            "curso",
            "forma_selecao",
        ]
