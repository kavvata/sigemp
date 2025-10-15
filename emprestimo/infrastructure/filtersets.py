from django.db.models import Q, QuerySet
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet

from emprestimo.models import Emprestimo, Ocorrencia


class EmprestimoFilterSet(FilterSet):
    texto = CharFilter(method="filtrar_texto")
    tem_ocorrencia = CharFilter(method="filtrar_tem_ocorrencia")

    def filtrar_texto(self, queryset: QuerySet[Emprestimo], _name, value):
        return queryset.filter(
            Q(aluno__nome__icontains=value)
            | Q(aluno__matricula__icontains=value)
            | Q(bem__descricao__icontains=value)
            | Q(bem__patrimonio__icontains=value)
        )

    def filtrar_tem_ocorrencia(self, queryset: QuerySet[Emprestimo], _name, value):
        if value == "s":
            return queryset.filter(ocorrencia__isnull=False)
        elif value == "n":
            return queryset.filter(ocorrencia__isnull=True)

        return queryset

    class Meta:
        model = Emprestimo
        fields = ["estado"]


class OcorrenciaFilterSet(FilterSet):
    aluno = CharFilter(method="filtrar_aluno")
    bem = CharFilter(method="filtrar_bem")
    eh_cancelado = CharFilter(method="filtrar_eh_cancelado")

    def filtrar_aluno(self, queryset: QuerySet[Emprestimo], _name, value):
        return queryset.filter(
            Q(emprestimo__aluno__nome__icontains=value)
            | Q(emprestimo__aluno__matricula__icontains=value)
        )

    def filtrar_bem(self, queryset: QuerySet[Emprestimo], _name, value):
        return queryset.filter(
            Q(emprestimo__bem__descricao__icontains=value)
            | Q(emprestimo__bem__patrimonio__icontains=value)
        )

    def filtrar_eh_cancelado(self, queryset: QuerySet[Emprestimo], _name, value):
        if value == "s":
            return queryset.filter(cancelado_em__isnull=False)
        elif value == "n":
            return queryset.filter(cancelado_em__isnull=True)

        return queryset

    class Meta:
        model = Ocorrencia
        fields = ["data_ocorrencia", "tipo"]
