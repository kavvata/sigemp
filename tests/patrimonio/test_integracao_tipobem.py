from unittest import mock
import pytest
from pytest_django.asserts import assertContains, assertTemplateUsed
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from patrimonio.models import TipoBem


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture()
def tipos_de_bem(db):
    tipos_de_bem = [
        {"id": 1, "descricao": "Projetor"},
        {"id": 2, "descricao": "Notebook Dell"},
        {"id": 3, "descricao": "Frasco laboratorio"},
    ]
    tipos_de_bem_models = [
        TipoBem.objects.get_or_create(descricao=tp["descricao"])[0]
        for tp in tipos_de_bem
    ]

    yield tipos_de_bem_models

    TipoBem.objects.filter(
        descricao__in=[tp["descricao"] for tp in tipos_de_bem]
    ).delete()


@pytest.mark.django_db
def test_listar_tipos_bem(tipos_de_bem, admin_client):
    response = admin_client.get(reverse_lazy("patrimonio:listar_tipos_bem"))

    for tipo in [tipo.descricao for tipo in tipos_de_bem]:
        assertContains(response, tipo)

    assertTemplateUsed("patrimonio/tipo_bem_list.html")


@pytest.mark.django_db
def test_listar_tipo_bem_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:listar_tipos_bem")
    response = client.get(url)

    assert response.status_code == 403


