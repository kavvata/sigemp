from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from patrimonio.models import TipoBem
from patrimonio.policies.django import DjangoTipoBemPolicy
from patrimonio.repositories.django import DjTipoBemRepository
from patrimonio.usecases import CadastrarTipoBemUsecase, ListarTiposBemUsecase


# Create your views here.
class ListarTiposBemView(ListView):
    model = TipoBem
    paginate_by = 20
    template_name = "patrimonio/tipo_bem/tipo_bem_list.html"
    context_object_name = "tipos_bem"

    def get_queryset(self):
        policy = DjangoTipoBemPolicy(self.request.user)
        repo = DjTipoBemRepository()
        usecase = ListarTiposBemUsecase(repo, policy)
        if not usecase.pode_listar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar tipos de bem."
            )
        result = usecase.execute()
        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        policy = DjangoTipoBemPolicy(self.request.user)
        repo = DjTipoBemRepository()

        usecase = CadastrarTipoBemUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context
