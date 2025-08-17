from django.shortcuts import render

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from ensino.models import Campus
from ensino.policies.django import DjangoCampusPolicy
from ensino.repositories.django import DjangoCampusRepository
from ensino.usecases import (
    ListarCampiUsecase,
    CadastrarCampusUsecase,
    EditarCampusUsecase,
    RemoverCampusUsecase,
)
from ensino.domain.entities import CampusEntity

from typing import Any

from ensino.presentation.forms import CampusForm

# Create your views here.


class ListarCampusView(ListView):
    model = Campus
    paginate_by = 10
    template_name = "ensino/campus/campus_list.html"
    context_object_name = "lista_campi"

    def get_queryset(self):
        policy = DjangoCampusPolicy(self.request.user)
        repo = DjangoCampusRepository()
        usecase = ListarCampiUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied("Voce nao tem permissao para visualizar campi")

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoCampusPolicy(self.request.user)
        repo = DjangoCampusRepository()

        usecase = CadastrarCampusUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarCampusView(CreateView):
    template_name = "ensino/campus/campus_form.html"
    form_class = CampusForm
    success_url = reverse_lazy("ensino:listar_campi")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoCampusRepository()
        policy = DjangoCampusPolicy(self.request.user)
        usecase = CadastrarCampusUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar bens móveis.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoCampusRepository()
        policy = DjangoCampusPolicy(self.request.user)
        usecase = CadastrarCampusUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar bens móveis.")

        novo_campus = CampusEntity(
            sigla=form.cleaned_data["sigla"],
            nome=form.cleaned_data["nome"],
        )
        result = usecase.execute(novo_campus)

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarCampusView(UpdateView):
    template_name = "ensino/campus/campus_form.html"
    queryset = Campus.objects.filter(removido_em__isnull=True)
    form_class = CampusForm
    success_url = reverse_lazy("ensino:listar_campi")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoCampusRepository()
        policy = DjangoCampusPolicy(self.request.user)
        usecase = EditarCampusUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_campus(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar bens móveis.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoCampusRepository()
        policy = DjangoCampusPolicy(self.request.user)
        usecase = EditarCampusUsecase(repo, policy)

        result = usecase.get_campus(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        campus = CampusEntity(
            id=form.instance.id,
            sigla=form.cleaned_data["sigla"],
            nome=form.cleaned_data["nome"],
        )
        result = usecase.execute(campus)

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_campus(request, pk):
    repo = DjangoCampusRepository()
    policy = DjangoCampusPolicy(request.user)

    usecase = RemoverCampusUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("ensino:listar_campi"))
