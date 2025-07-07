from django.urls import path

from . import views


app_name = "patrimonio"
urlpatterns = [
    path(
        "tipo_bem/",
        views.ListarTiposBemView.as_view(),
        name="listar_tipos_bem",
    ),
    path(
        "tipo_bem/add",
        views.CriarTipoBemView.as_view(),
        name="criar_tipo_bem",
    ),
    path(
        "tipo_bem/change/<int:pk>/",
        views.EditarTipoBemView.as_view(),
        name="editar_tipo_bem",
    ),
    path(
        "tipo_bem/delete/<int:pk>/",
        views.remover_tipobem,
        name="remover_tipo_bem",
    ),
    path(
        "estado_conservacao/",
        views.ListarEstadosConservacaoView.as_view(),
        name="listar_estados_conservacao",
    ),
    path(
        "estado_conservacao/add",
        views.CriarEstadoConservacaoView.as_view(),
        name="criar_estado_conservacao",
    ),
    path(
        "estado_conservacao/change/<int:pk>/",
        views.EditarEstadoConservacaoView.as_view(),
        name="editar_estado_conservacao",
    ),
    path(
        "estado_conservacao/delete/<int:pk>/",
        views.remover_estado_conservacao,
        name="remover_estado_conservacao",
    ),
    path(
        "grau_fragilidade/",
        views.ListarGrauFragilidadeView.as_view(),
        name="listar_grau_fragilidade",
    ),
    path(
        "grau_fragilidade/add",
        views.CriarGrauFragilidadeView.as_view(),
        name="criar_grau_fragilidade",
    ),
    path(
        "grau_fragilidade/change/<int:pk>/",
        views.EditarGrauFragilidadeView.as_view(),
        name="editar_grau_fragilidade",
    ),
    path(
        "grau_fragilidade/delete/<int:pk>/",
        views.remover_grau_fragilidade,
        name="remover_grau_fragilidade",
    ),
]
