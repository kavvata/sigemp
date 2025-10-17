from typing import Any

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from emprestimo.domain.entities import (
    OcorrenciaEntity,
    TipoOcorrenciaEntity,
    EmprestimoEntity,
)
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.infrastructure.services.django import DjangoWeasyPDFService
from emprestimo.models import Ocorrencia, TipoOcorrencia, Emprestimo
from emprestimo.policies.django import (
    DjangoOcorrenciaPolicy,
    DjangoTipoOcorrenciaPolicy,
    DjangoEmprestimoPolicy,
)
from emprestimo.presentation.forms import (
    CancelarOcorrenciaForm,
    EmprestimoFilterForm,
    OcorrenciaFilterForm,
    OcorrenciaForm,
    TipoOcorrenciaForm,
    CriarEmprestimoForm,
)
from emprestimo.repositories.django import (
    DjangoTipoOcorrenciaRepository,
    DjangoEmprestimoRepository,
    DjangoOcorrenciaRepository,
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
from emprestimo.usecases.emprestimo_usecases import (
    GerarTermoDevolucaoUsecase,
    GerarTermoResponsabilidadeUsecase,
    RegistrarDevolucaoEmprestimoUsecase,
)
from emprestimo.usecases.ocorrencia_usecases import (
    CancelarOcorrenciaUsecase,
    ListarOcorrenciasAlunoUsecase,
    ListarOcorrenciasBemUsecase,
    ListarOcorrenciasEmprestimoUsecase,
    ListarOcorrenciasUsecase,
    RegistrarOcorrenciaUsecase,
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
            messages.error(self.request, result.mensagem)
            return []

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
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("emprestimo:criar_tipo_ocorrencia"))

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
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy(
                    "emprestimo:editar_tipo_ocorrencia", args=[form.instance.id]
                ),
            )

        tipo_ocorrencia = TipoOcorrenciaEntity(
            id=form.instance.id,
            descricao=form.cleaned_data["descricao"],
        )
        result = usecase.execute(tipo_ocorrencia)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy(
                    "emprestimo:editar_tipo_ocorrencia", args=[form.instance.id]
                ),
            )

        return redirect(self.success_url)


def remover_tipo_ocorrencia(request, pk):
    repo = DjangoTipoOcorrenciaRepository()
    policy = DjangoTipoOcorrenciaPolicy(request.user)

    usecase = RemoverTipoOcorrenciaUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        messages.error(request, result.mensagem)
        return redirect(
            reverse_lazy("emprestimo:editar_tipo_ocorrencia", args=[pk]),
        )

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

        self.filter = EmprestimoFilterForm(self.request.GET or None)

        if self.filter.is_valid():
            result = usecase.execute(self.filter.cleaned_data)
        else:
            result = usecase.execute()

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoEmprestimoPolicy(self.request.user)
        repo = DjangoEmprestimoRepository()

        usecase = CadastrarEmprestimoUsecase(repo, policy)

        context["filter"] = self.filter
        context["pode_criar"] = usecase.pode_criar()

        return context


def atualizar_tabela_emprestimo_view(request: HttpRequest):
    if not request.headers.get("HX-Request"):
        return redirect("emprestimo:listar_emprestimos")

    policy = DjangoEmprestimoPolicy(request.user)
    repo = DjangoEmprestimoRepository()
    usecase = ListarEmprestimosUsecase(repo, policy)

    if not usecase.pode_listar():
        raise PermissionDenied("Voce nao tem permissao para visualizar empréstimo.")

    filter = EmprestimoFilterForm(request.GET or None)

    if filter.is_valid():
        result = usecase.execute(filter.cleaned_data)
    else:
        result = usecase.execute()

    if not result:
        messages.error(request, result.mensagem)
        return []

    emprestimos = result.value

    return render(
        request,
        "emprestimo/emprestimo/partials/table.html",
        {"emprestimos": emprestimos},
    )


class CriarEmprestimoView(CreateView):
    template_name = "partials/form.html"

    form_class = CriarEmprestimoForm
    success_url = reverse_lazy("emprestimo:listar_emprestimos")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = CadastrarEmprestimoUsecase(repo, policy)

        if not request.headers.get("HX-Request"):
            return redirect("emprestimo:listar_emprestimos")

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
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("emprestimo:criar_emprestimo"))

        return redirect(self.success_url)


class VisualizarEmprestimoView(DetailView):
    model = Emprestimo
    template_name = "emprestimo/emprestimo/emprestimo_detail.html"
    context_object_name = "emprestimo"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        emprestimo: Emprestimo = context["emprestimo"]

        ocorrencia_policy = DjangoOcorrenciaPolicy(self.request.user)
        ocorrencia_repo = DjangoOcorrenciaRepository()
        usecase = ListarOcorrenciasEmprestimoUsecase(ocorrencia_repo, ocorrencia_policy)

        resultado = usecase.execute(emprestimo.id)

        if not resultado:
            messages.error(resultado.mensagem)
            return context

        context["lista_ocorrencias"] = resultado.value

        return context


class EditarEmprestimoView(UpdateView):
    template_name = "partials/form.html"
    queryset = Emprestimo.objects.filter(removido_em__isnull=True)
    form_class = CriarEmprestimoForm
    success_url = reverse_lazy("emprestimo:atualizar_tabela_emprestimo")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = EditarEmprestimoUsecase(repo, policy)

        if not request.headers.get("HX-Request"):
            return redirect(self.success_url)

        if not usecase.pode_editar(usecase.get_emprestimo(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar emprestimo.")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["submit_url"] = reverse_lazy(
            "emprestimo:editar_emprestimo", args=[context["form"].instance.id]
        )
        context["remove_url"] = reverse_lazy(
            "emprestimo:remover_emprestimo", args=[context["form"].instance.id]
        )
        context["modal_title"] = f"Editar Emprestimo #{context['form'].instance.id}"
        return context

    def form_valid(self, form):
        repo = DjangoEmprestimoRepository()
        policy = DjangoEmprestimoPolicy(self.request.user)
        usecase = EditarEmprestimoUsecase(repo, policy)

        if not usecase.pode_editar(form.instance):
            raise PermissionDenied("Voce nao tem permissao para editar emprestimo.")

        result = usecase.get_emprestimo(form.instance.id)
        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("emprestimo:listar_emprestimos"))

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
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("emprestimo:editar_emprestimo"))

        return redirect(self.success_url)


def remover_emprestimo(request, pk):
    repo = DjangoEmprestimoRepository()
    policy = DjangoEmprestimoPolicy(request.user)

    if not policy.pode_remover(repo.buscar_por_id(pk)):
        raise PermissionDenied("Voce nao tem permissao para remover emprestimo.")

    usecase = RemoverEmprestimoUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        messages.error(request, result.mensagem)
        return redirect(reverse_lazy("emprestimo:visualizar_emprestimo", args=[pk]))

    return redirect(reverse_lazy("emprestimo:atualizar_tabela_emprestimo"))


def registrar_devolucao_view(request, pk):
    repo = DjangoEmprestimoRepository()
    policy = DjangoEmprestimoPolicy(request.user)

    emprestimo = repo.buscar_por_id(pk)

    usecase = RegistrarDevolucaoEmprestimoUsecase(repo, policy)
    resultado = usecase.execute(emprestimo)

    if not resultado:
        messages.error(request, resultado.mensagem)
        return redirect(
            reverse_lazy("emprestimo:visualizar_emprestimo", args=[emprestimo.id])
        )

    return redirect(
        reverse_lazy("emprestimo:visualizar_emprestimo", args=[emprestimo.id])
    )


def gerar_termo_responsabilidade_view(request, pk):
    repo = DjangoEmprestimoRepository()
    policy = DjangoEmprestimoPolicy(request.user)
    service = DjangoWeasyPDFService(request)

    try:
        emprestimo = repo.buscar_por_id(pk)
    except Emprestimo.DoesNotExist:
        raise Http404

    if not policy.pode_gerar_termos(emprestimo):
        raise PermissionDenied(
            "Voce nao tem permissao para gerar termos de emprestimo."
        )
    usecase = GerarTermoResponsabilidadeUsecase(repo, policy, service)

    result = usecase.execute(emprestimo)

    if not result:
        messages.error(request, result.mensagem)
        return redirect(
            reverse_lazy("emprestimo:visualizar_emprestimo", args=[emprestimo.id])
        )

    response = result.value
    return response


def gerar_termo_devolucao_view(request, pk):
    repo = DjangoEmprestimoRepository()
    policy = DjangoEmprestimoPolicy(request.user)
    service = DjangoWeasyPDFService(request)

    try:
        emprestimo = repo.buscar_por_id(pk)
    except Emprestimo.DoesNotExist:
        raise Http404

    if not policy.pode_gerar_termos(emprestimo):
        raise PermissionDenied(
            "Voce nao tem permissao para gerar termos de emprestimo."
        )
    usecase = GerarTermoDevolucaoUsecase(repo, policy, service)

    result = usecase.execute(emprestimo)

    if not result:
        messages.error(request, result.mensagem)
        return redirect(
            reverse_lazy("emprestimo:visualizar_emprestimo", args=[emprestimo.id])
        )

    response = result.value
    return response


class ListarOcorrenciasView(ListView):
    model = Ocorrencia
    paginate_by = 10
    template_name = "emprestimo/ocorrencia/ocorrencia_list.html"
    context_object_name = "ocorrencias"

    def get_queryset(self):
        policy = DjangoOcorrenciaPolicy(self.request.user)
        repo = DjangoOcorrenciaRepository()
        usecase = ListarOcorrenciasUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Você não tem permissão para visualizar ocorrências."
            )

        self.filter = OcorrenciaFilterForm(self.request.GET or None)
        if self.filter.is_valid():
            result = usecase.execute(self.filter.cleaned_data)
        else:
            result = usecase.execute()

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoOcorrenciaPolicy(self.request.user)
        repo = DjangoOcorrenciaRepository()

        usecase = RegistrarOcorrenciaUsecase(repo, policy)

        context["filter"] = self.filter
        context["pode_criar"] = usecase.pode_criar()

        return context


class VisualizarOcorrenciaView(DetailView):
    model = Ocorrencia
    template_name = "emprestimo/ocorrencia/ocorrencia_detail.html"
    context_object_name = "ocorrencia"


class ListarOcorrenciasAlunoView(ListView):
    model = Ocorrencia
    paginate_by = 10
    template_name = "emprestimo/ocorrencia/ocorrencia_list.html"
    context_object_name = "ocorrencias"

    def get_queryset(self):
        aluno_id = self.kwargs["aluno_id"]
        policy = DjangoOcorrenciaPolicy(self.request.user)
        repo = DjangoOcorrenciaRepository()
        usecase = ListarOcorrenciasAlunoUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Você não tem permissão para visualizar ocorrências."
            )

        result = usecase.execute(aluno_id)

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["filtro_aluno"] = True
        return context


class ListarOcorrenciasBemView(ListView):
    model = Ocorrencia
    paginate_by = 10
    template_name = "emprestimo/ocorrencia/ocorrencia_list.html"
    context_object_name = "ocorrencias"

    def get_queryset(self):
        bem_id = self.kwargs["bem_id"]
        policy = DjangoOcorrenciaPolicy(self.request.user)
        repo = DjangoOcorrenciaRepository()
        usecase = ListarOcorrenciasBemUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Você não tem permissão para visualizar ocorrências."
            )

        result = usecase.execute(bem_id)

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["filtro_bem"] = True
        return context


class ListarOcorrenciasEmprestimoView(ListView):
    model = Ocorrencia
    paginate_by = 10
    template_name = "emprestimo/ocorrencia/ocorrencia_list.html"
    context_object_name = "ocorrencias"

    def get_queryset(self):
        emprestimo_id = self.kwargs["emprestimo_id"]
        policy = DjangoOcorrenciaPolicy(self.request.user)
        repo = DjangoOcorrenciaRepository()
        usecase = ListarOcorrenciasEmprestimoUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Você não tem permissão para visualizar ocorrências."
            )

        result = usecase.execute(emprestimo_id)

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["filtro_emprestimo"] = True
        return context


class RegistrarOcorrenciaView(CreateView):
    template_name = "emprestimo/ocorrencia/ocorrencia_form.html"
    form_class = OcorrenciaForm
    success_url = reverse_lazy("emprestimo:listar_ocorrencias")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoOcorrenciaRepository()
        policy = DjangoOcorrenciaPolicy(self.request.user)
        usecase = RegistrarOcorrenciaUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Você não tem permissão para registrar ocorrências.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoOcorrenciaRepository()
        policy = DjangoOcorrenciaPolicy(self.request.user)
        usecase = RegistrarOcorrenciaUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Você não tem permissão para registrar ocorrências.")

        nova_ocorrencia = OcorrenciaEntity(
            data_ocorrencia=form.cleaned_data["data_ocorrencia"],
            emprestimo_id=form.cleaned_data["emprestimo"].id,
            tipo_id=form.cleaned_data["tipo"].id,
        )
        result = usecase.execute(nova_ocorrencia)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("emprestimo:registrar_ocorrencia"))

        return redirect(self.success_url)


def registrar_ocorrencia_ao_emprestimo(request, emprestimo_id: int):
    success_url = reverse_lazy(
        "emprestimo:visualizar_emprestimo",
        args=[emprestimo_id],
    )

    template_name = "emprestimo/ocorrencia/ocorrencia_form.html"

    repo = DjangoOcorrenciaRepository()
    policy = DjangoOcorrenciaPolicy(request.user)
    usecase = RegistrarOcorrenciaUsecase(repo, policy)

    if not usecase.pode_criar():
        raise PermissionDenied("Você não tem permissão para registrar ocorrências.")

    e = get_object_or_404(Emprestimo, pk=emprestimo_id)

    form = OcorrenciaForm(request.POST or None, emprestimo=e)

    if form.is_valid():
        if not usecase.pode_criar():
            raise PermissionDenied("Você não tem permissão para registrar ocorrências.")

        nova_ocorrencia = OcorrenciaEntity(
            data_ocorrencia=form.cleaned_data["data_ocorrencia"],
            emprestimo_id=form.cleaned_data["emprestimo"].id,
            tipo_id=form.cleaned_data["tipo"].id,
        )
        result = usecase.execute(nova_ocorrencia)

        if not result:
            messages.error(request, result.mensagem)
            return redirect(
                reverse_lazy(
                    "emprestimo:visualizar_emprestimo",
                    args=[emprestimo_id],
                )
            )

        return redirect(success_url)

    return render(request, template_name, {"form": form})


class CancelarOcorrenciaView(UpdateView):
    template_name = "emprestimo/ocorrencia/ocorrencia_form.html"
    queryset = Ocorrencia.objects
    form_class = CancelarOcorrenciaForm
    success_url = reverse_lazy("emprestimo:listar_ocorrencias")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoOcorrenciaRepository()
        policy = DjangoOcorrenciaPolicy(self.request.user)
        usecase = CancelarOcorrenciaUsecase(repo, policy)

        ocorrencia = usecase.buscar_por_id(kwargs.get("pk", None))

        if not ocorrencia:
            raise Http404("Ocorrência não encontrada.")

        if not usecase.pode_remover(ocorrencia):
            raise PermissionDenied("Você não tem permissão para cancelar ocorrências.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoOcorrenciaRepository()
        policy = DjangoOcorrenciaPolicy(self.request.user)
        usecase = CancelarOcorrenciaUsecase(repo, policy)

        ocorrencia = usecase.buscar_por_id(form.instance.id)

        if not usecase.pode_remover(ocorrencia):
            raise PermissionDenied("Você não tem permissão para cancelar ocorrências.")

        result = usecase.execute(
            form.instance.id, form.cleaned_data["motivo_cancelamento"]
        )

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy(
                    "emprestimo:cancelar_ocorrencia",
                    args=[ocorrencia.id],
                )
            )

        return redirect(self.success_url)
