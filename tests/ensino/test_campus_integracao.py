import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from ensino.domain.entities import CampusEntity
from ensino.models import Campus


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def campus_entity():
    return CampusEntity(sigla="PNG", nome="Paranaguá")


@pytest.fixture
def campus(db):
    entity = CampusEntity(sigla="PNG", nome="Paranaguá")
    model, _criado = Campus.objects.get_or_create(entity.to_dict())
    yield model

    model.delete()


def lista_campi(db):
    lista_entities = [
        CampusEntity(sigla="PNG", nome="Paranaguá"),
        CampusEntity(sigla="CWB", nome="Curitiba"),
        CampusEntity(sigla="CSV", nome="Cascavel"),
        CampusEntity(sigla="CLB", nome="Colombo"),
        CampusEntity(sigla="LND", nome="Londrina"),
    ]

    campi_models = [
        Campus.objects.get_or_create(e.to_dict())[0] for e in lista_entities
    ]
    yield campi_models

    Campus.objects.filter(sigla__in=[e.sigla for e in lista_entities]).delete()


@pytest.mark.django_db
def test_listar_campi(lista_campi, admin_client):
    response = admin_client.get(reverse_lazy("ensino:listar_campi"))
    for nome in [campus.nome for campus in lista_campi]:
        assertContains(response, nome)

    assertTemplateUsed(response, "ensino/campus/campus_list.html")


@pytest.mark.django_db
def test_nao_pode_listar_campi(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("ensino:listar_campi")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_campus(admin_client, campus_entity: CampusEntity):
    url = reverse_lazy("ensino:criar_campus")
    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/campus/campus_form.html")

    assert response.status_code == 200

    form_data = campus_entity.to_dict(["timestamps", "id"])

    response = admin_client.post(url, form_data, follow=True)

    assert response.status_code == 200
    assert Campus.objects.filter(nome=campus_entity.nome).exists()
    assertContains(response, campus_entity.nome)
    assertTemplateUsed(response, "ensino/campus/campus_list.html")


@pytest.mark.django_db
def test_nao_pode_criar_campus(client, test_user, campus_entity: CampusEntity):
    client.force_login(test_user)

    url = reverse_lazy("ensino:criar_campus")

    response = client.get(url)

    assert response.status_code == 403

    form_data = campus_entity.to_dict(["timestamps", "id"])

    response = client.post(url, form_data, follow=True)

    assert response.status_code == 403
    assert not Campus.objects.filter(nome=campus_entity.nome).exists()
    assertTemplateNotUsed(response, "patrimonio/campus/campus_form.html")


@pytest.mark.django_db
def test_editar_campus(admin_client, campus_entity: CampusEntity, campus):
    url = reverse_lazy("patrimonio:editar_bem", args=[campus.pk])

    response = admin_client.get(url)

    assertTemplateUsed(response, "ensino/campus/campus_form.html")
    assert response.status_code == 200

    original = campus.sigla
    campus_entity.id = campus.id
    campus_entity.sigla = "PGUA"
    form_data = campus_entity.to_dict(exclude=["timestamps"])

    response = admin_client.post(url, form_data, follow=True)
    campus.refresh_from_db()
    assert campus.sigla == campus_entity.sigla
    assertContains(response, campus_entity.nome)
    assertTemplateUsed(response, "patrimonio/campus/campus_form.html")


@pytest.mark.django_db
def test_nao_pode_editar_campus(client, test_user, campus_entity: CampusEntity, campus):
    client.force_login(test_user)
    url = reverse_lazy("patrimonio:editar_bem", args=[campus.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = campus.sigla

    campus_entity.id = campus.id
    campus_entity.sigla = "PGUA"
    form_data = campus_entity.to_dict(exclude=["timestamps"])

    response = client.post(url, form_data, follow=True)
    assertTemplateNotUsed(response, "ensino/campus/campus_list.html")
    campus.refresh_from_db()
    assert campus.sigla == original


@pytest.mark.django_db
def test_remover_campus(admin_client, campus):
    url = reverse_lazy("ensino:remover_campus", args=[campus.pk])

    response = admin_client.post(url, follow=True)

    campus.refresh_from_db()

    assert response.status_code == 200
    assert campus.removido_em is not None

    response = admin_client.get(reverse_lazy("ensino:listar_campi"))
    assertNotContains(response, campus.descricao)


@pytest.mark.django_db
def test_nao_pode_remover_campus(client, test_user, campus):
    client.force_login(test_user)

    url = reverse_lazy("ensino:remover_campus", args=[campus.pk])
    response = client.post(url, follow=True)

    campus.refresh_from_db()
    assert campus.removido_em is None
    assert response.status_code == 403
