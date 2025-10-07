from django.db.models import Q, QuerySet
from django_filters.filters import BooleanFilter, CharFilter
from django_filters.filterset import FilterSet

from emprestimo.domain.types import EmprestimoEstadoEnum
from patrimonio.models import Bem


class BemFilterSet(FilterSet):
    texto = CharFilter(method="filtrar_texto")
    eh_disponivel = BooleanFilter(method="filtrar_disponivel")

    def filtrar_texto(self, queryset: QuerySet[Bem], name, value):
        return queryset.filter(
            Q(descricao__icontains=value)
            | Q(patrimonio__icontains=value)
            | Q(tipo__descricao__icontains=value)
            | Q(marca_modelo__marca__icontains=value)
            | Q(marca_modelo__modelo__icontains=value)
        )

    def filtrar_disponivel(self, queryset: QuerySet[Bem], name, value):
        return (
            queryset.filter(emprestimo__estado=EmprestimoEstadoEnum.ATIVO)
            if value
            else queryset
        )

    class Meta:
        model = Bem
        fields = ["tipo"]
