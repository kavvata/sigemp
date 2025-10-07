from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet

from ensino.models import Aluno


class AlunoFilterSet(FilterSet):
    nome = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Aluno
        fields = ["nome", "curso"]
