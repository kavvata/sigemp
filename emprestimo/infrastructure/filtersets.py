from django.db.models import Q, QuerySet
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet

from emprestimo.models import Emprestimo


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
