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
]
