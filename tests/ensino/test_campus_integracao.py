import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)
from requests import delete

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

    campi_models = [Campus.objects.get_or_create(e.to_dict)[0] for e in lista_entities]
    yield campi_models

    Campus.objects.filter(sigla__in=[e.sigla for e in lista_entities]).delete()


@pytest.mark.django_db
def test_listar_campi(lista_campi, admin_client):
    raise NotImplementedError


@pytest.mark.django_db
def test_nao_pode_listar_campi(lista_campi, client, test_user):
    raise NotImplementedError


@pytest.mark.django_db
def test_criar_campus(admin_client, campus_entity: CampusEntity):
    raise NotImplementedError


@pytest.mark.django_db
def test_nao_pode_criar_campus(client, test_user, campus_entity: CampusEntity):
    raise NotImplementedError


@pytest.mark.django_db
def test_editar_campus(admin_client, campus_entity: CampusEntity, campus):
    raise NotImplementedError


@pytest.mark.django_db
def test_nao_pode_editar_campus(client, test_user, campus_entity: CampusEntity, campus):
    raise NotImplementedError


@pytest.mark.django_db
def test_remover_bem(admin_client, campus):
    raise NotImplementedError


@pytest.mark.django_db
def test_nao_pode_remover_bem(client, test_user, campus):
    raise NotImplementedError
