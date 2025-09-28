from django.urls import path

from . import views

app_name = "emprestimo"

urlpatterns = [
    path(
        "tipo_ocorrencia/",
        views.ListarTipoOcorrenciaView.as_view(),
        name="listar_tipos_ocorrencia",
    ),
    path(
        "tipo_ocorrencia/add",
        views.CriarTipoOcorrenciaView.as_view(),
        name="criar_tipo_ocorrencia",
    ),
    path(
        "tipo_ocorrencia/change/<int:pk>/",
        views.EditarTipoOcorrenciaView.as_view(),
        name="editar_tipo_ocorrencia",
    ),
    path(
        "tipo_ocorrencia/delete/<int:pk>/",
        views.remover_tipo_ocorrencia,
        name="remover_tipo_ocorrencia",
    ),
    path(
        "emprestimo/",
        views.ListarEmprestimoView.as_view(),
        name="listar_emprestimos",
    ),
    path(
        "emprestimo/add",
        views.CriarEmprestimoView.as_view(),
        name="criar_emprestimo",
    ),
    path(
        "emprestimo/change/<int:pk>/",
        views.EditarEmprestimoView.as_view(),
        name="editar_emprestimo",
    ),
    path(
        "emprestimo/delete/<int:pk>/",
        views.remover_emprestimo,
        name="remover_emprestimo",
    ),
]
