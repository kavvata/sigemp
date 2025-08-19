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
    path(
        "curso/",
        views.ListarCursoView.as_view(),
        name="listar_cursos",
    ),
    path(
        "curso/add",
        views.CriarCursoView.as_view(),
        name="criar_curso",
    ),
    path(
        "curso/change/<int:pk>/",
        views.EditarCursoView.as_view(),
        name="editar_curso",
    ),
    path(
        "curso/delete/<int:pk>/",
        views.remover_curso,
        name="remover_curso",
    ),
]
