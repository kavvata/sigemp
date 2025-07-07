from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from patrimonio.models import EstadoConservacao, GrauFragilidade, TipoBem
from patrimonio.policies.django import (
    DjangoEstadoConservacaoPolicy,
    DjangoGrauFragilidadePolicy,
    DjangoTipoBemPolicy,
)
from patrimonio.presentation.forms import (
    EstadoConservacaoForm,
    GrauFragilidadeForm,
    TipoBemForm,
)
from patrimonio.repositories.django import (
    DjangoEstadoConservacaoRepository,
    DjangoGrauFragilidadeRepository,
    DjTipoBemRepository,
)
from patrimonio.usecases import (
    CadastrarEstadoConservacaoUsecase,
    CadastrarGrauFragilidadeUsecase,
    CadastrarTipoBemUsecase,
    EditarEstadoConservacaoUsecase,
    EditarGrauFragilidadeUsecase,
    EditarTipoBemUsecase,
    ListarEstadosConservacaoUsecase,
    ListarGrauFragilidadeUsecase,
    ListarTiposBemUsecase,
    RemoverEstadoConservacaoUsecase,
    RemoverGrauFragilidadeUsecase,
    RemoverTipoBemUsecase,
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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = CadastrarTipoBemUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar tipo de bem.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = CadastrarTipoBemUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar tipo de bem.")

        result = usecase.execute(form.cleaned_data["descricao"])

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarTipoBemView(UpdateView):
    template_name = "patrimonio/tipo_bem/tipo_bem_form.html"
    form_class = TipoBemForm
    queryset = TipoBem.objects.filter(removido_em__isnull=True)
    success_url = reverse_lazy("patrimonio:listar_tipos_bem")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = EditarTipoBemUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_tipo_bem(pk)):
            raise PermissionDenied("Voce nao tem permissao para criar tipo de bem.")

        return super().get(request, *args, **kwargs)

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

        return redirect(self.success_url)


def remover_tipobem(request, pk):
    repo = DjTipoBemRepository()
    policy = DjangoTipoBemPolicy(request.user)
    usecase = RemoverTipoBemUsecase(repo, policy)

    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("patrimonio:listar_tipos_bem"))


class ListarEstadosConservacaoView(ListView):
    model = EstadoConservacao
    paginate_by = 10
    template_name = "patrimonio/estado_conservacao/estado_conservacao_list.html"
    context_object_name = "estados_conservacao"

    def get_queryset(self):
        policy = DjangoEstadoConservacaoPolicy(self.request.user)
        repo = DjangoEstadoConservacaoRepository()
        usecase = ListarEstadosConservacaoUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar estados de conservacao"
            )

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoEstadoConservacaoPolicy(self.request.user)
        repo = DjangoEstadoConservacaoRepository()

        usecase = CadastrarEstadoConservacaoUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarEstadoConservacaoView(CreateView):
    template_name = "patrimonio/estado_conservacao/estado_conservacao_form.html"
    form_class = EstadoConservacaoForm
    success_url = reverse_lazy("patrimonio:listar_estados_conservacao")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoEstadoConservacaoRepository()
        policy = DjangoEstadoConservacaoPolicy(self.request.user)
        usecase = CadastrarEstadoConservacaoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied(
                "Voce nao tem permissao para criar estado de conservacao."
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoEstadoConservacaoRepository()
        policy = DjangoEstadoConservacaoPolicy(self.request.user)
        usecase = CadastrarEstadoConservacaoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied(
                "Voce nao tem permissao para criar estado de conservacao."
            )
        result = usecase.execute(
            form.cleaned_data["descricao"], form.cleaned_data["nivel"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarEstadoConservacaoView(UpdateView):
    template_name = "patrimonio/estado_conservacao/estado_conservacao_form.html"
    queryset = EstadoConservacao.objects.filter(removido_em__isnull=True)
    form_class = EstadoConservacaoForm
    success_url = reverse_lazy("patrimonio:listar_estados_conservacao")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoEstadoConservacaoRepository()
        policy = DjangoEstadoConservacaoPolicy(self.request.user)
        usecase = EditarEstadoConservacaoUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_estado_conservacao(pk)):
            raise PermissionDenied(
                "Voce nao tem permissao para criar estado de conservação."
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoEstadoConservacaoRepository()
        policy = DjangoEstadoConservacaoPolicy(self.request.user)
        usecase = EditarEstadoConservacaoUsecase(repo, policy)

        result = usecase.get_estado_conservacao(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        result = usecase.execute(
            form.instance.id, form.cleaned_data["descricao"], form.cleaned_data["nivel"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_estado_conservacao(request, pk):
    repo = DjangoEstadoConservacaoRepository()
    policy = DjangoEstadoConservacaoPolicy(request.user)
    usecase = RemoverEstadoConservacaoUsecase(repo, policy)

    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("patrimonio:listar_estados_conservacao"))


class ListarGrauFragilidadeView(ListView):
    model = GrauFragilidade
    paginate_by = 10
    template_name = "patrimonio/grau_fragilidade/grau_fragilidade_list.html"
    context_object_name = "lista_grau_fragilidade"

    def get_queryset(self):
        policy = DjangoGrauFragilidadePolicy(self.request.user)
        repo = DjangoGrauFragilidadeRepository()
        usecase = ListarGrauFragilidadeUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar estados de conservacao"
            )

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoGrauFragilidadePolicy(self.request.user)
        repo = DjangoGrauFragilidadeRepository()

        usecase = CadastrarGrauFragilidadeUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarGrauFragilidadeView(CreateView):
    template_name = "patrimonio/grau_fragilidade/grau_fragilidade_form.html"
    form_class = GrauFragilidadeForm
    success_url = reverse_lazy("patrimonio:listar_grau_fragilidade")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoGrauFragilidadeRepository()
        policy = DjangoGrauFragilidadePolicy(self.request.user)
        usecase = CadastrarGrauFragilidadeUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied(
                "Voce nao tem permissao para criar estado de conservacao."
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoGrauFragilidadeRepository()
        policy = DjangoGrauFragilidadePolicy(self.request.user)
        usecase = CadastrarGrauFragilidadeUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied(
                "Voce nao tem permissao para criar estado de conservacao."
            )
        result = usecase.execute(
            form.cleaned_data["descricao"], form.cleaned_data["nivel"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarGrauFragilidadeView(UpdateView):
    template_name = "patrimonio/grau_fragilidade/grau_fragilidade_form.html"
    queryset = GrauFragilidade.objects.filter(removido_em__isnull=True)
    form_class = GrauFragilidadeForm
    success_url = reverse_lazy("patrimonio:listar_grau_fragilidade")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoGrauFragilidadeRepository()
        policy = DjangoGrauFragilidadePolicy(self.request.user)
        usecase = EditarGrauFragilidadeUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_grau_fragilidade(pk)):
            raise PermissionDenied(
                "Voce nao tem permissao para criar estado de conservação."
            )

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoGrauFragilidadeRepository()
        policy = DjangoGrauFragilidadePolicy(self.request.user)
        usecase = EditarGrauFragilidadeUsecase(repo, policy)

        result = usecase.get_grau_fragilidade(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        result = usecase.execute(
            form.instance.id, form.cleaned_data["descricao"], form.cleaned_data["nivel"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_grau_fragilidade(request, pk):
    repo = DjangoGrauFragilidadeRepository()
    policy = DjangoGrauFragilidadePolicy(request.user)
    usecase = RemoverGrauFragilidadeUsecase(repo, policy)

    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("patrimonio:listar_grau_fragilidade"))
