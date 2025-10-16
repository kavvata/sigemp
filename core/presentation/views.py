from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_not_required
from django.urls import reverse
from django.utils import timezone
from django.template.loader import render_to_string

from core.presentation.forms import LoginForm
from core.repositories.django import DjUserRepository
from core.usecases import login_usecase

from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.models import Emprestimo, Ocorrencia
from emprestimo.policies.django import DjangoEmprestimoPolicy
from ensino.models import Aluno
from patrimonio.models import Bem, EstadoConservacao


# Create your views here.
@login_not_required
def login_view(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            repo = DjUserRepository()

            result = login_usecase(
                form.cleaned_data["username"],
                form.cleaned_data["password"],
                repo,
            )

            if not result:
                messages.error(request, result.mensagem)
                return redirect(reverse("core:login"))

            user: User = result.value
            login(request, user)
            return redirect(reverse("core:home"))

    return render(request, "registration/login.html", {"form": LoginForm})


def home_view(request: HttpRequest):
    count_emprestimos_ativos: int = Emprestimo.objects.filter(
        estado=EmprestimoEstadoEnum.ATIVO
    ).count()

    count_emprestimos_vencendo: int = Emprestimo.objects.filter(
        data_devolucao_prevista=timezone.now()
    ).count()

    emprestimos_recentes = Emprestimo.objects.filter(
        data_emprestimo__gt=timezone.now() - timedelta(days=14),
        estado=EmprestimoEstadoEnum.ATIVO,
    ).order_by("-data_emprestimo")[:3]

    count_alunos = Aluno.objects.all().count()

    count_novos_alunos = Aluno.objects.filter(
        criado_em__gt=timezone.now() - timedelta(days=30)
    ).count()

    count_bens_disponiveis = (
        Bem.objects.exclude(emprestimo__estado=EmprestimoEstadoEnum.ATIVO)
        .distinct()
        .count()
    )

    count_bens_com_ocorrencias = (
        Bem.objects.filter(
            emprestimo__ocorrencia__isnull=False,
            emprestimo__estado=EmprestimoEstadoEnum.ATIVO,
        )
        .distinct()
        .count()
    )

    count_ocorrencias = Ocorrencia.objects.filter(cancelado_em__isnull=True).count()

    emprestimo_policy = DjangoEmprestimoPolicy(request.user)

    pode_criar_emprestimo = emprestimo_policy.pode_criar()

    context = {
        "count_emprestimos_ativos": count_emprestimos_ativos,
        "count_emprestimos_vencendo": count_emprestimos_vencendo,
        "emprestimos_recentes": emprestimos_recentes,
        "count_alunos": count_alunos,
        "count_novos_alunos": count_novos_alunos,
        "count_bens_disponiveis": count_bens_disponiveis,
        "count_bens_com_ocorrencias": count_bens_com_ocorrencias,
        "count_ocorrencias": count_ocorrencias,
        "pode_criar_emprestimo": pode_criar_emprestimo,
    }

    return render(request, "core/home.html", context=context)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("core:login"))


def search(request):
    q = request.GET.get("q", "")
    print(request.GET)

    items = Aluno.objects.filter(nome__icontains=q)
    html = render_to_string(
        "partials/autocomplete_results.html",
        {"items": items},
    )
    return HttpResponse(html)
