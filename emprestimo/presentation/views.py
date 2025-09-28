from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from emprestimo.domain.entities import TipoOcorrenciaEntity, EmprestimoEntity
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.models import TipoOcorrencia, Emprestimo
from emprestimo.policies.django import (
    DjangoTipoOcorrenciaPolicy,
    DjangoEmprestimoPolicy,
)
from emprestimo.presentation.forms import TipoOcorrenciaForm, CriarEmprestimoForm
from emprestimo.repositories.django import (
    DjangoTipoOcorrenciaRepository,
    DjangoEmprestimoRepository,
)
from emprestimo.usecases import (
    CadastrarTipoOcorrenciaUsecase,
    EditarTipoOcorrenciaUsecase,
    ListarTiposOcorrenciaUsecase,
    RemoverTipoOcorrenciaUsecase,
    ListarEmprestimosUsecase,
    CadastrarEmprestimoUsecase,
    EditarEmprestimoUsecase,
    RemoverEmprestimoUsecase,
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


class ListarEmprestimoView(ListView):
    model = Emprestimo
    paginate_by = 10
    template_name = "emprestimo/emprestimo/emprestimo_list.html"
    context_object_name = "emprestimos"

    def get_queryset(self):
        policy = DjangoEmprestimoPolicy(self.request.user)
        repo = DjangoEmprestimoRepository()
        usecase = ListarEmprestimosUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied("Voce nao tem permissao para visualizar empréstimo.")

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoEmprestimoPolicy(self.request.user)
        repo = DjangoEmprestimoRepository()

        usecase = CadastrarEmprestimoUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarEmprestimoView(CreateView):
    template_name = "emprestimo/emprestimo/emprestimo_form.html"
    form_class = CriarEmprestimoForm
    success_url = reverse_lazy("emprestimo:listar_emprestimos")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = CadastrarEmprestimoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar emprestimo.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = CadastrarEmprestimoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar emprestimo.")

        novo_emprestimo = EmprestimoEntity(
            aluno_id=form.cleaned_data["aluno"].id,
            bem_id=form.cleaned_data["bem"].id,
            data_emprestimo=form.cleaned_data["data_emprestimo"],
            data_devolucao_prevista=form.cleaned_data["data_devolucao_prevista"],
            estado=EmprestimoEstadoEnum.ATIVO,
            observacoes=form.cleaned_data["observacoes"],
        )
        result = usecase.execute(novo_emprestimo)

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class VisualizarEmprestimoView(DetailView):
    model = Emprestimo
    template_name = "emprestimo/emprestimo/emprestimo_detail.html"
    context_object_name = "emprestimo"


class EditarEmprestimoView(UpdateView):
    template_name = "emprestimo/emprestimo/emprestimo_form.html"
    queryset = Emprestimo.objects.filter(removido_em__isnull=True)
    form_class = CriarEmprestimoForm
    success_url = reverse_lazy("emprestimo:listar_emprestimos")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = EditarEmprestimoUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_emprestimo(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar emprestimo.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = EditarEmprestimoUsecase(repo, policy)

        result = usecase.get_emprestimo(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        emprestimo = EmprestimoEntity(
            id=form.instance.id,
            aluno_id=form.cleaned_data["aluno"].id,
            bem_id=form.cleaned_data["bem"].id,
            data_emprestimo=form.cleaned_data["data_emprestimo"],
            data_devolucao_prevista=form.cleaned_data["data_devolucao_prevista"],
            observacoes=form.cleaned_data["observacoes"],
            estado=EmprestimoEstadoEnum.ATIVO,
        )
        result = usecase.execute(emprestimo)

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_emprestimo(request, pk):
    repo = DjangoEmprestimoRepository()
    policy = DjangoEmprestimoPolicy(request.user)

    usecase = RemoverEmprestimoUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("emprestimo:listar_emprestimos"))
