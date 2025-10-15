from typing import Any

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, ListView, UpdateView

from emprestimo.policies.django import DjangoOcorrenciaPolicy
from emprestimo.repositories.django import DjangoOcorrenciaRepository
from emprestimo.usecases.ocorrencia_usecases import ListarOcorrenciasAlunoUsecase
from ensino.domain.entities import (
    AlunoEntity,
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
)
from ensino.models import Aluno, Campus, Curso, FormaSelecao
from ensino.policies.django import (
    DjangoAlunoPolicy,
    DjangoCampusPolicy,
    DjangoCursoPolicy,
    DjangoFormaSelecaoPolicy,
)
from ensino.presentation.forms import (
    AlunoFilterForm,
    AlunoForm,
    CampusForm,
    CursoForm,
    FormaSelecaoForm,
)
from ensino.repositories.django import (
    DjangoAlunoRepository,
    DjangoCampusRepository,
    DjangoCursoRepository,
    DjangoFormaSelecaoRepository,
)
from ensino.usecases import (
    CadastrarAlunoUsecase,
    CadastrarCampusUsecase,
    CadastrarCursoUsecase,
    CadastrarFormaSelecaoUsecase,
    EditarAlunoUsecase,
    EditarCampusUsecase,
    EditarCursoUsecase,
    EditarFormaSelecaoUsecase,
    ListarAlunosUsecase,
    ListarCampiUsecase,
    ListarCursosUsecase,
    ListarFormasSelecaoUsecase,
    RemoverAlunoUsecase,
    RemoverCampusUsecase,
    RemoverCursoUsecase,
    RemoverFormaSelecaoUsecase,
)

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
            messages.error(self.request, result.mensagem)
            return []

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
            raise PermissionDenied("Voce nao tem permissao para criar campus.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoCampusRepository()
        policy = DjangoCampusPolicy(self.request.user)
        usecase = CadastrarCampusUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar campus.")

        novo_campus = CampusEntity(
            sigla=form.cleaned_data["sigla"],
            nome=form.cleaned_data["nome"],
        )
        result = usecase.execute(novo_campus)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("ensino:criar_campus"))

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
            raise PermissionDenied("Voce nao tem permissao para editar campus.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoCampusRepository()
        policy = DjangoCampusPolicy(self.request.user)
        usecase = EditarCampusUsecase(repo, policy)

        result = usecase.get_campus(form.instance.id)
        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_campus", args=[form.instance.id])
            )

        campus = CampusEntity(
            id=form.instance.id,
            sigla=form.cleaned_data["sigla"],
            nome=form.cleaned_data["nome"],
        )
        result = usecase.execute(campus)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_campus", args=[form.instance.id])
            )

        return redirect(self.success_url)


def remover_campus(request, pk):
    repo = DjangoCampusRepository()
    policy = DjangoCampusPolicy(request.user)

    usecase = RemoverCampusUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        messages.error(request, result.mensagem)
        return redirect(reverse("ensino:editar_campus", args=[pk]))

    return redirect(reverse_lazy("ensino:listar_campi"))


class ListarCursoView(ListView):
    model = Curso
    paginate_by = 10
    template_name = "ensino/curso/curso_list.html"
    context_object_name = "lista_cursos"

    def get_queryset(self):
        policy = DjangoCursoPolicy(self.request.user)
        repo = DjangoCursoRepository()
        usecase = ListarCursosUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied("Voce nao tem permissao para visualizar cursos")

        result = usecase.execute()

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoCursoPolicy(self.request.user)
        repo = DjangoCursoRepository()

        usecase = CadastrarCursoUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarCursoView(CreateView):
    template_name = "ensino/curso/curso_form.html"
    form_class = CursoForm
    success_url = reverse_lazy("ensino:listar_cursos")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoCursoRepository()
        policy = DjangoCursoPolicy(self.request.user)
        usecase = CadastrarCursoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar curso.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoCursoRepository()
        policy = DjangoCursoPolicy(self.request.user)
        usecase = CadastrarCursoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar curso.")

        novo_curso = CursoEntity(
            sigla=form.cleaned_data["sigla"],
            nome=form.cleaned_data["nome"],
            campus_id=form.cleaned_data["campus"].id,
        )
        result = usecase.execute(novo_curso)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("ensino:criar_curso"))

        return redirect(self.success_url)


class EditarCursoView(UpdateView):
    template_name = "ensino/curso/curso_form.html"
    queryset = Curso.objects.filter(removido_em__isnull=True)
    form_class = CursoForm
    success_url = reverse_lazy("ensino:listar_cursos")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoCursoRepository()
        policy = DjangoCursoPolicy(self.request.user)
        usecase = EditarCursoUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_curso(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar cursos.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoCursoRepository()
        policy = DjangoCursoPolicy(self.request.user)
        usecase = EditarCursoUsecase(repo, policy)

        result = usecase.get_curso(form.instance.id)
        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_curso", args=[form.instance.id])
            )

        curso = CursoEntity(
            id=form.instance.id,
            sigla=form.cleaned_data["sigla"],
            nome=form.cleaned_data["nome"],
            campus_id=form.cleaned_data["campus"],
        )
        result = usecase.execute(curso)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_curso", args=[form.instance.id])
            )

        return redirect(self.success_url)


def remover_curso(request, pk):
    repo = DjangoCursoRepository()
    policy = DjangoCursoPolicy(request.user)

    usecase = RemoverCursoUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        messages.error(request, result.mensagem)
        return redirect(reverse_lazy("ensino:editar_curso", args=[pk]))

    return redirect(reverse_lazy("ensino:listar_cursos"))


class ListarFormaSelecaoView(ListView):
    model = FormaSelecao
    paginate_by = 10
    template_name = "ensino/forma_selecao/formaselecao_list.html"
    context_object_name = "lista_formas_selecao"

    def get_queryset(self):
        policy = DjangoFormaSelecaoPolicy(self.request.user)
        repo = DjangoFormaSelecaoRepository()
        usecase = ListarFormasSelecaoUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied(
                "Voce nao tem permissao para visualizar formas de seleção."
            )

        result = usecase.execute()

        if not result:
            messages.error(self.request, result.mensagem)
            return []

        return result.value

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        policy = DjangoFormaSelecaoPolicy(self.request.user)
        repo = DjangoFormaSelecaoRepository()

        usecase = CadastrarFormaSelecaoUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarFormaSelecaoView(CreateView):
    template_name = "ensino/forma_selecao/formaselecao_form.html"
    form_class = FormaSelecaoForm
    success_url = reverse_lazy("ensino:listar_formas_selecao")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoFormaSelecaoRepository()
        policy = DjangoFormaSelecaoPolicy(self.request.user)
        usecase = CadastrarFormaSelecaoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar forma_selecao.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoFormaSelecaoRepository()
        policy = DjangoFormaSelecaoPolicy(self.request.user)
        usecase = CadastrarFormaSelecaoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar forma_selecao.")

        novo_forma_selecao = FormaSelecaoEntity(
            descricao=form.cleaned_data["descricao"],
            periodo_inicio=form.cleaned_data["periodo_inicio"],
            periodo_fim=form.cleaned_data["periodo_fim"],
        )
        result = usecase.execute(novo_forma_selecao)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("ensino:criar_forma_selecao"))

        return redirect(self.success_url)


class EditarFormaSelecaoView(UpdateView):
    template_name = "ensino/forma_selecao/formaselecao_form.html"
    queryset = FormaSelecao.objects.filter(removido_em__isnull=True)
    form_class = FormaSelecaoForm
    success_url = reverse_lazy("ensino:listar_formas_selecao")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoFormaSelecaoRepository()
        policy = DjangoFormaSelecaoPolicy(self.request.user)
        usecase = EditarFormaSelecaoUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_forma_selecao(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar forma_selecao.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoFormaSelecaoRepository()
        policy = DjangoFormaSelecaoPolicy(self.request.user)
        usecase = EditarFormaSelecaoUsecase(repo, policy)

        result = usecase.get_forma_selecao(form.instance.id)
        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_forma_selecao", args=[form.instance.id])
            )

        forma_selecao = FormaSelecaoEntity(
            id=form.instance.id,
            descricao=form.cleaned_data["descricao"],
            periodo_inicio=form.cleaned_data["periodo_inicio"],
            periodo_fim=form.cleaned_data["periodo_fim"],
        )
        result = usecase.execute(forma_selecao)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_forma_selecao", args=[form.instance.id])
            )

        return redirect(self.success_url)


def remover_forma_selecao(request, pk):
    repo = DjangoFormaSelecaoRepository()
    policy = DjangoFormaSelecaoPolicy(request.user)

    usecase = RemoverFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        messages.error(request, result.mensagem)
        return redirect(reverse_lazy("ensino:editar_forma_selecao", args=[pk]))

    return redirect(reverse_lazy("ensino:listar_formas_selecao"))


class ListarAlunoView(ListView):
    model = Aluno
    paginate_by = 10
    template_name = "ensino/aluno/aluno_list.html"
    context_object_name = "lista_alunos"

    def get_queryset(self):
        policy = DjangoAlunoPolicy(self.request.user)
        repo = DjangoAlunoRepository()
        usecase = ListarAlunosUsecase(repo, policy)

        if not usecase.pode_listar():
            raise PermissionDenied("Voce nao tem permissao para visualizar alunos.")

        self.filter = AlunoFilterForm(self.request.GET or None)

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
        policy = DjangoAlunoPolicy(self.request.user)
        repo = DjangoAlunoRepository()

        context["filter"] = AlunoFilterForm(self.request.GET or None)
        usecase = CadastrarAlunoUsecase(repo, policy)

        context["pode_criar"] = usecase.pode_criar()

        return context


class CriarAlunoView(CreateView):
    template_name = "ensino/aluno/aluno_form.html"
    form_class = AlunoForm
    success_url = reverse_lazy("ensino:listar_alunos")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        repo = DjangoAlunoRepository()
        policy = DjangoAlunoPolicy(self.request.user)
        usecase = CadastrarAlunoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar aluno.")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        repo = DjangoAlunoRepository()
        policy = DjangoAlunoPolicy(self.request.user)
        usecase = CadastrarAlunoUsecase(repo, policy)

        if not usecase.pode_criar():
            raise PermissionDenied("Voce nao tem permissao para criar aluno.")

        novo_aluno = AlunoEntity(
            nome=form.cleaned_data["nome"],
            cpf=form.cleaned_data["cpf"],
            matricula=form.cleaned_data["matricula"],
            nome_responsavel=form.cleaned_data["nome_responsavel"],
            email=form.cleaned_data["email"],
            telefone=form.cleaned_data["telefone"],
            curso_id=form.cleaned_data["curso"].id,
            forma_selecao_id=form.cleaned_data["forma_selecao"].id,
        )
        result = usecase.execute(novo_aluno)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(reverse_lazy("ensino:criar_aluno"))

        return redirect(self.success_url)


class EditarAlunoView(UpdateView):
    template_name = "ensino/aluno/aluno_form.html"
    queryset = Aluno.objects.filter(removido_em__isnull=True)
    form_class = AlunoForm
    success_url = reverse_lazy("ensino:listar_alunos")

    def get(
        self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        repo = DjangoAlunoRepository()
        policy = DjangoAlunoPolicy(self.request.user)
        usecase = EditarAlunoUsecase(repo, policy)

        if not usecase.pode_editar(usecase.get_aluno(pk)):
            raise PermissionDenied("Voce nao tem permissao para editar aluno.")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        aluno: Aluno = context["form"].instance

        ocorrencia_policy = DjangoOcorrenciaPolicy(self.request.user)
        ocorrencia_repo = DjangoOcorrenciaRepository()

        usecase = ListarOcorrenciasAlunoUsecase(ocorrencia_repo, ocorrencia_policy)
        resultado = usecase.execute(aluno.id)

        if not resultado:
            messages.error(resultado.mensagem)
            return context

        context["lista_ocorrencias"] = resultado.value

        return context

    def form_valid(self, form):
        repo = DjangoAlunoRepository()
        policy = DjangoAlunoPolicy(self.request.user)
        usecase = EditarAlunoUsecase(repo, policy)

        result = usecase.get_aluno(form.instance.id)
        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_aluno", args=[form.instance.id])
            )

        aluno = AlunoEntity(
            id=form.instance.id,
            nome=form.cleaned_data["nome"],
            cpf=form.cleaned_data["cpf"],
            matricula=form.cleaned_data["matricula"],
            nome_responsavel=form.cleaned_data["nome_responsavel"],
            email=form.cleaned_data["email"],
            telefone=form.cleaned_data["telefone"],
            curso_id=form.cleaned_data["curso"].id,
            forma_selecao_id=form.cleaned_data["forma_selecao"].id,
        )
        result = usecase.execute(aluno)

        if not result:
            messages.error(self.request, result.mensagem)
            return redirect(
                reverse_lazy("ensino:editar_aluno", args=[form.instance.id])
            )

        return redirect(self.success_url)


def remover_aluno(request, pk):
    repo = DjangoAlunoRepository()
    policy = DjangoAlunoPolicy(request.user)

    usecase = RemoverAlunoUsecase(repo, policy)
    result = usecase.execute(pk)
    if not result:
        messages.error(request, result.mensagem)
        return redirect(reverse_lazy("ensino:editar_aluno", args=[pk]))

    return redirect(reverse_lazy("ensino:listar_alunos"))
