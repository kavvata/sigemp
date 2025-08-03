from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from patrimonio.models import (
    EstadoConservacao,
    GrauFragilidade,
    MarcaModelo,
    TipoBem,
    Bem,
)
from patrimonio.policies.django import (
    DjangoEstadoConservacaoPolicy,
    DjangoGrauFragilidadePolicy,
    DjangoMarcaModeloPolicy,
    DjangoTipoBemPolicy,
    DjangoBemPolicy,
)
from patrimonio.presentation.forms import (
    EstadoConservacaoForm,
    GrauFragilidadeForm,
    MarcaModeloForm,
    TipoBemForm,
    BemForm,
)
from patrimonio.repositories.django import (
    DjangoEstadoConservacaoRepository,
    DjangoGrauFragilidadeRepository,
    DjangoMarcaModeloRepository,
    DjangoTipoBemRepository,
    DjangoBemRepository,
)
from patrimonio.usecases import (
    CadastrarEstadoConservacaoUsecase,
    CadastrarGrauFragilidadeUsecase,
    CadastrarMarcaModeloUsecase,
    CadastrarTipoBemUsecase,
    CadastrarBemUsecase,
    EditarEstadoConservacaoUsecase,
    EditarGrauFragilidadeUsecase,
    EditarMarcaModeloUsecase,
    EditarTipoBemUsecase,
    EditarBemUsecase,
    ListarEstadosConservacaoUsecase,
    ListarGrauFragilidadeUsecase,
    ListarMarcaModeloUsecase,
    ListarTiposBemUsecase,
    ListarBensUsecase,
    RemoverEstadoConservacaoUsecase,
    RemoverGrauFragilidadeUsecase,
    RemoverMarcaModeloUsecase,
    RemoverTipoBemUsecase,
    RemoverBemUsecase,
)


# Create your views here.
class ListarTiposBemView(ListView):
    model = TipoBem
    paginate_by = 10
    template_name = "patrimonio/tipo_bem/tipo_bem_list.html"
    context_object_name = "tipos_bem"

    def get_queryset(self):
        policy = DjangoTipoBemPolicy(self.request.user)
        repo = DjangoTipoBemRepository()
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
        repo = DjangoTipoBemRepository()

        usecase = CadastrarTipoBemUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarTipoBemView(CreateView):
    template_name = "patrimonio/tipo_bem/tipo_bem_form.html"
    form_class = TipoBemForm
    success_url = reverse_lazy("patrimonio:listar_tipos_bem")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = CadastrarTipoBemUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar tipo de bem.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoTipoBemRepository()
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
        repo = DjangoTipoBemRepository()
        policy = DjangoTipoBemPolicy(self.request.user)
        usecase = EditarTipoBemUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_tipo_bem(pk)):
            raise PermissionDenied("Voce nao tem permissao para criar tipo de bem.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoTipoBemRepository()
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
    repo = DjangoTipoBemRepository()
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


class ListarMarcaModeloView(ListView):
    model = MarcaModelo
    paginate_by = 10
    template_name = "patrimonio/marca_modelo/marca_modelo_list.html"
    context_object_name = "lista_marca_modelo"

    def get_queryset(self):
        policy = DjangoMarcaModeloPolicy(self.request.user)
        repo = DjangoMarcaModeloRepository()
        usecase = ListarMarcaModeloUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar marcas/modelos"
            )

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoMarcaModeloPolicy(self.request.user)
        repo = DjangoMarcaModeloRepository()

        usecase = CadastrarMarcaModeloUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarMarcaModeloView(CreateView):
    template_name = "patrimonio/marca_modelo/marca_modelo_form.html"
    form_class = MarcaModeloForm
    success_url = reverse_lazy("patrimonio:listar_marca_modelo")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoMarcaModeloRepository()
        policy = DjangoMarcaModeloPolicy(self.request.user)
        usecase = CadastrarMarcaModeloUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar marcas/modelos.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoMarcaModeloRepository()
        policy = DjangoMarcaModeloPolicy(self.request.user)
        usecase = CadastrarMarcaModeloUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar marcas/modelos.")
        result = usecase.execute(
            form.cleaned_data["marca"], form.cleaned_data["modelo"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarMarcaModeloView(UpdateView):
    template_name = "patrimonio/marca_modelo/marca_modelo_form.html"
    queryset = MarcaModelo.objects.filter(removido_em__isnull=True)
    form_class = MarcaModeloForm
    success_url = reverse_lazy("patrimonio:listar_marca_modelo")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoMarcaModeloRepository()
        policy = DjangoMarcaModeloPolicy(self.request.user)
        usecase = EditarMarcaModeloUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_marca_modelo(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar marca/modelo.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoMarcaModeloRepository()
        policy = DjangoMarcaModeloPolicy(self.request.user)
        usecase = EditarMarcaModeloUsecase(repo, policy)

        result = usecase.get_marca_modelo(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        result = usecase.execute(
            form.instance.id, form.cleaned_data["marca"], form.cleaned_data["modelo"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_marca_modelo(request, pk):
    repo = DjangoMarcaModeloRepository()
    policy = DjangoMarcaModeloPolicy(request.user)

    usecase = RemoverMarcaModeloUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("patrimonio:listar_marca_modelo"))


class ListarBemView(ListView):
    model = Bem
    paginate_by = 10
    template_name = "patrimonio/bem/bem_list.html"
    context_object_name = "lista_bem"

    def get_queryset(self):
        policy = DjangoBemPolicy(self.request.user)
        repo = DjangoBemRepository()
        usecase = ListarBensUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied("Voce nao tem permissao para visualizar bens móveis")

        result = usecase.execute()

        if not result:
            raise PermissionDenied(result.mensagem)

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoBemPolicy(self.request.user)
        repo = DjangoBemRepository()

        usecase = CadastrarBemUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarBemView(CreateView):
    template_name = "patrimonio/bem/bem_form.html"
    form_class = BemForm
    success_url = reverse_lazy("patrimonio:listar_bem")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoBemRepository()
        policy = DjangoBemPolicy(self.request.user)
        usecase = CadastrarBemUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar bens móveis.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoBemRepository()
        policy = DjangoBemPolicy(self.request.user)
        usecase = CadastrarBemUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar bens móveis.")
        result = usecase.execute(
            form.cleaned_data["marca"], form.cleaned_data["modelo"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


class EditarBemView(UpdateView):
    template_name = "patrimonio/bem/bem_form.html"
    queryset = Bem.objects.filter(removido_em__isnull=True)
    form_class = BemForm
    success_url = reverse_lazy("patrimonio:listar_bem")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoBemRepository()
        policy = DjangoBemPolicy(self.request.user)
        usecase = EditarBemUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_bem(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar marca/modelo.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoBemRepository()
        policy = DjangoBemPolicy(self.request.user)
        usecase = EditarBemUsecase(repo, policy)

        result = usecase.get_bem(form.instance.id)
        if not result:
            raise PermissionDenied(result.mensagem)

        result = usecase.execute(
            form.instance.id, form.cleaned_data["marca"], form.cleaned_data["modelo"]
        )

        if not result:
            raise PermissionDenied(result.mensagem)

        return redirect(self.success_url)


def remover_bem(request, pk):
    repo = DjangoBemRepository()
    policy = DjangoBemPolicy(request.user)

    usecase = RemoverBemUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        raise PermissionDenied(result.mensagem)

    return redirect(reverse_lazy("patrimonio:listar_bem"))
