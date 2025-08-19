import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from core.types import ResultError, ResultSuccess
from ensino.domain.entities import CampusEntity, CursoEntity
from ensino.models import Campus, Curso


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def campus(db):
    entity = CampusEntity(id=1, sigla="PNG", nome="Paranaguá")
    model, _criado = Campus.objects.get_or_create(
        entity.to_dict(
            [
                "timestamps",
                "campus_sigla",
            ]
        )
    )
    yield model

    model.delete()


@pytest.fixture
def lista_campi(db):
    lista_entities = [
        CampusEntity(id=1, sigla="PNG", nome="Paranaguá"),
        CampusEntity(id=2, sigla="CWB", nome="Curitiba"),
        CampusEntity(id=3, sigla="CSV", nome="Cascavel"),
        CampusEntity(id=4, sigla="CLB", nome="Colombo"),
        CampusEntity(id=5, sigla="LND", nome="Londrina"),
    ]

    campi_models = [
        Campus.objects.get_or_create(**e.to_dict())[0] for e in lista_entities
    ]
    yield campi_models

    Campus.objects.filter(sigla__in=[e.sigla for e in lista_entities]).delete()


@pytest.fixture
def curso_entity(campus):
    return CursoEntity(
        sigla="TADS",
        nome="Técnologo em Análise e Desenvolvimento de Sistemas",
        campus_id=1,
    )


@pytest.fixture
def curso(campus):
    e = CursoEntity(
        sigla="TADS",
        nome="Técnologo em Análise e Desenvolvimento de Sistemas",
        campus_id=1,
    )
    model, _criado = Curso.objects.get_or_create(**e.to_dict(["timestamps", "sigla"]))
    yield model

    model.delete()


@pytest.fixture
def lista_cursos(db, lista_campi):
    lista_entities = [
        CursoEntity(
            sigla="TMI",
            nome="Tecnologia em Manutenção Industrial",
            campus_id=1,
        ),
        CursoEntity(
            sigla="LFIS",
            nome="Licenciatura em Física",
            campus_id=1,
        ),
        CursoEntity(
            sigla="LCS",
            nome="Licenciatura em Ciências Sociais",
            campus_id=1,
        ),
        CursoEntity(
            sigla="TADS",
            nome="Tecnologia em Análise e Desenvolvimento de Sistemas",
            campus_id=1,
        ),
        CursoEntity(
            sigla="TGA",
            nome="Tecnologia em Gestão Ambiental",
            campus_id=1,
        ),
        CursoEntity(
            sigla="MEC",
            nome="Técnico em Mecânica",
            campus_id=1,
        ),
        CursoEntity(
            sigla="INFO",
            nome="Técnico em Informática",
            campus_id=1,
        ),
        CursoEntity(
            sigla="MAMB",
            nome="Técnico em Meio Ambiente",
            campus_id=1,
        ),
        CursoEntity(
            sigla="TPC",
            nome="Técnico em Produção Cultural",
            campus_id=1,
        ),
    ]

    lista_models = [
        Curso.objects.get_or_create(
            **e.to_dict(
                [
                    "timestamps",
                    "id",
                    "campus_sigla",
                ]
            )
        )[0]
        for e in lista_entities
    ]
    yield lista_models

    Curso.objects.filter(sigla__in=[e.sigla for e in lista_entities]).delete()


@pytest.mark.django_db
def test_listar_cursos(lista_cursos, admin_client):
    response = admin_client.get(reverse_lazy("ensino:listar_cursos"))
    for nome in [campus.nome for campus in lista_cursos]:
        assertContains(response, nome)

    assertTemplateUsed(response, "ensino/curso/curso_list.html")


@pytest.mark.django_db
def test_nao_pode_listar_cursos(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("ensino:listar_cursos")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_curso(admin_client, curso_entity: CursoEntity):
    url = reverse_lazy("ensino:criar_curso")
    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/curso/curso_form.html")

    assert response.status_code == 200

    form_data = curso_entity.to_dict(["timestamps", "id", "campus_sigla"])

    response = admin_client.post(url, form_data, follow=True)
    assert response.status_code == 200

    assert Curso.objects.filter(nome=curso_entity.nome).exists()
    assertContains(response, curso_entity.nome)
    assertTemplateUsed(response, "ensino/curso/curso_list.html")


@pytest.mark.django_db
def test_nao_pode_criar_curso(client, test_user, curso_entity: CursoEntity):
    client.force_login(test_user)

    url = reverse_lazy("ensino:criar_curso")

    response = client.get(url)

    assert response.status_code == 403

    form_data = curso_entity.to_dict(["timestamps", "id", "campus_sigla"])

    response = client.post(url, form_data, follow=True)

    assert response.status_code == 403
    assert not Curso.objects.filter(nome=curso_entity.nome).exists()
    assertTemplateNotUsed(response, "ensino/curso/curso_form.html")


@pytest.mark.django_db
def test_editar_curso(admin_client, curso_entity: CursoEntity, curso):
    url = reverse_lazy("ensino:editar_curso", args=[curso.pk])

    response = admin_client.get(url)

    assertTemplateUsed(response, "ensino/curso/curso_form.html")
    assert response.status_code == 200

    original = curso.sigla
    curso_entity.id = curso.id
    curso_entity.sigla = "PGUA"
    form_data = curso_entity.to_dict(exclude=["timestamps", "campus_sigla"])

    response = admin_client.post(url, form_data, follow=True)
    curso.refresh_from_db()
    assert curso.sigla == curso_entity.sigla
    assertContains(response, curso_entity.nome)
    assertTemplateUsed(response, "ensino/curso/curso_list.html")


@pytest.mark.django_db
def test_nao_pode_editar_curso(client, test_user, curso_entity: CursoEntity, curso):
    client.force_login(test_user)
    url = reverse_lazy("ensino:editar_curso", args=[curso.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = curso.sigla

    curso_entity.id = curso.id
    curso_entity.sigla = "PGUA"
    form_data = curso_entity.to_dict(exclude=["timestamps", "campus_sigla"])

    response = client.post(url, form_data, follow=True)
    assertTemplateNotUsed(response, "ensino/curso/curso_list.html")
    curso.refresh_from_db()
    assert curso.sigla == original


@pytest.mark.django_db
def test_remover_curso(admin_client, curso):
    url = reverse_lazy("ensino:remover_curso", args=[curso.pk])

    response = admin_client.post(url, follow=True)

    curso.refresh_from_db()

    assert response.status_code == 200
    assert curso.removido_em is not None

    response = admin_client.get(reverse_lazy("ensino:listar_cursos"))
    assertNotContains(response, curso.nome)


@pytest.mark.django_db
def test_nao_pode_remover_curso(client, test_user, curso):
    client.force_login(test_user)

    url = reverse_lazy("ensino:remover_curso", args=[curso.pk])
    response = client.post(url, follow=True)

    curso.refresh_from_db()
    assert curso.removido_em is None
    assert response.status_code == 403
