from typing import Optional
from django import forms
from django.forms.widgets import DateInput

from core.widgets import ModelAutocompleteWidget
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.models import Emprestimo, Ocorrencia, TipoOcorrencia
from ensino.models import Aluno
from patrimonio.models import Bem


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

    aluno = forms.ModelChoiceField(
        Aluno.objects,
        widget=ModelAutocompleteWidget(Aluno),
    )

    bem = forms.ModelChoiceField(
        Bem.objects,
        widget=ModelAutocompleteWidget(Bem),
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


class OcorrenciaForm(forms.ModelForm):
    data_ocorrencia = forms.DateField(
        label="Data da ocorrência",
        widget=DateInput(attrs={"type": "date"}),
    )

    emprestimo = forms.ModelChoiceField(
        queryset=Emprestimo.objects.all().order_by("-data_emprestimo", "estado")
    )

    def __init__(self, *args, **kwargs) -> None:
        e: Optional[Emprestimo] = None

        if "emprestimo" in kwargs.keys():
            e = kwargs.pop("emprestimo")

        super().__init__(*args, **kwargs)

        if e:
            self.fields["emprestimo"].initial = e
            self.fields["emprestimo"].disabled = True

    class Meta:
        model = Ocorrencia
        fields = ["tipo", "emprestimo", "data_ocorrencia", "descricao"]


class CancelarOcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ["motivo_cancelamento"]


class EmprestimoFilterForm(forms.Form):
    texto = forms.CharField(max_length=255, required=False)
    estado = forms.ChoiceField(
        choices=[(None, "---------")] + EmprestimoEstadoEnum.choices(),
        required=False,
    )
    tem_ocorrencia = forms.ChoiceField(
        label="Possui ocorrência?",
        required=False,
        choices=[("", "---------"), ("s", "Sim"), ("n", "Não")],
    )


class OcorrenciaFilterForm(forms.Form):
    aluno = forms.CharField(max_length=255, required=False)
    bem = forms.CharField(max_length=255, required=False)
    data_ocorrencia = forms.DateField(
        label="Data da ocorrência",
        required=False,
        widget=DateInput(attrs={"type": "date"}),
    )
    tipo = forms.ModelChoiceField(
        queryset=TipoOcorrencia.objects,
        required=False,
    )
    eh_cancelado = forms.ChoiceField(
        label="Cancelado?",
        required=False,
        choices=[("", "---------"), ("s", "Sim"), ("n", "Não")],
    )
