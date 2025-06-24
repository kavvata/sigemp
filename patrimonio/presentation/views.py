from typing import Any

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from patrimonio.models import TipoBem
from patrimonio.policies.django import DjangoTipoBemPolicy
from patrimonio.presentation.forms import TipoBemForm
from patrimonio.repositories.django import DjTipoBemRepository
from patrimonio.usecases import (
    CadastrarTipoBemUsecase,
    EditarTipoBemUsecase,
    ListarTiposBemUsecase,
)


# Create your views here.
class ListarTiposBemView(ListView):
    model = TipoBem
    paginate_by = 10
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


class CriarTipoBemView(CreateView):
    template_name = "patrimonio/tipo_bem/tipo_bem_form.html"
    form_class = TipoBemForm
    success_url = reverse_lazy("patrimonio:listar_tipos_bem")

    def form_valid(self, form):
        repo = DjTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = CadastrarTipoBemUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar tipos de bem."
            )

        result = usecase.execute(form.cleaned_data["descricao"])

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarTipoBemView(UpdateView):
    template_name = "patrimonio/tipo_bem/tipo_bem_form.html"
    form_class = TipoBemForm
    queryset = TipoBem.objects.filter(ativo=True)
    success_url = reverse_lazy("patrimonio:listar_tipos_bem")

    def form_valid(self, form):
        repo = DjTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = EditarTipoBemUsecase(repo, policy)

        result = usecase.get_tipo_bem(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        result = usecase.execute(form.instance.id, form.cleaned_data["descricao"])

        if not result:
            raise PermissionDenied(result.mensagem)

        return super().form_valid(form)
