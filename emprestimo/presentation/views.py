from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from emprestimo.domain.entities import TipoOcorrenciaEntity
from emprestimo.models import TipoOcorrencia
from emprestimo.policies.django import DjangoTipoOcorrenciaPolicy
from emprestimo.presentation.forms import TipoOcorrenciaForm
from emprestimo.repositories.django import DjangoTipoOcorrenciaRepository
from emprestimo.usecases import (
    CadastrarTipoOcorrenciaUsecase,
    EditarTipoOcorrenciaUsecase,
    ListarTiposOcorrenciaUsecase,
    RemoverTipoOcorrenciaUsecase,
)


# Create your views here.
class ListarTipoOcorrenciaView(ListView):
    model = TipoOcorrencia
    paginate_by = 10
    template_name = "emprestimo/tipo_ocorrencia/tipoocorrencia_list.html"
    context_object_name = "tipos_ocorrencia"

    def get_queryset(self):
        policy = DjangoTipoOcorrenciaPolicy(self.request.user)
        repo = DjangoTipoOcorrenciaRepository()
        usecase = ListarTiposOcorrenciaUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar tipos de ocorrência."
            )

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoTipoOcorrenciaPolicy(self.request.user)
        repo = DjangoTipoOcorrenciaRepository()

        usecase = CadastrarTipoOcorrenciaUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarTipoOcorrenciaView(CreateView):
    template_name = "emprestimo/tipo_ocorrencia/tipoocorrencia_form.html"
    form_class = TipoOcorrenciaForm
    success_url = reverse_lazy("emprestimo:listar_tipos_ocorrencia")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoTipoOcorrenciaRepository()
        policy = DjangoTipoOcorrenciaPolicy(self.request.user)
        usecase = CadastrarTipoOcorrenciaUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar tipo_ocorrencia.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoTipoOcorrenciaRepository()
        policy = DjangoTipoOcorrenciaPolicy(self.request.user)
        usecase = CadastrarTipoOcorrenciaUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar tipo_ocorrencia.")

        novo_tipo_ocorrencia = TipoOcorrenciaEntity(
            descricao=form.cleaned_data["descricao"],
        )
        result = usecase.execute(novo_tipo_ocorrencia)

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarTipoOcorrenciaView(UpdateView):
    template_name = "emprestimo/tipo_ocorrencia/tipoocorrencia_form.html"
    queryset = TipoOcorrencia.objects.filter(removido_em__isnull=True)
    form_class = TipoOcorrenciaForm
    success_url = reverse_lazy("emprestimo:listar_tipos_ocorrencia")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoTipoOcorrenciaRepository()
        policy = DjangoTipoOcorrenciaPolicy(self.request.user)
        usecase = EditarTipoOcorrenciaUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_tipo_ocorrencia(pk)):
            raise PermissionDenied(
                "Voce nao tem permissao para editar tipo_ocorrencia."
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoTipoOcorrenciaRepository()
        policy = DjangoTipoOcorrenciaPolicy(self.request.user)
        usecase = EditarTipoOcorrenciaUsecase(repo, policy)

        result = usecase.get_tipo_ocorrencia(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        tipo_ocorrencia = TipoOcorrenciaEntity(
            id=form.instance.id,
            descricao=form.cleaned_data["descricao"],
        )
        result = usecase.execute(tipo_ocorrencia)

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_tipo_ocorrencia(request, pk):
    repo = DjangoTipoOcorrenciaRepository()
    policy = DjangoTipoOcorrenciaPolicy(request.user)

    usecase = RemoverTipoOcorrenciaUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("emprestimo:listar_tipos_ocorrencia"))
