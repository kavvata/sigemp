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
]
