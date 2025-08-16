from django.urls import path

from . import views


app_name = "ensino"

urlpatterns = [
    path(
        "campus/",
        views.ListarCampusView.as_view(),
        name="listar_campi",
    ),
    path(
        "campus/add",
        views.CriarCampusView.as_view(),
        name="criar_campus",
    ),
    path(
        "campus/change/<int:pk>/",
        views.EditarCampusView.as_view(),
        name="editar_campus",
    ),
    path(
        "campus/delete/<int:pk>/",
        views.remover_campus,
        name="remover_campus",
    ),
]
