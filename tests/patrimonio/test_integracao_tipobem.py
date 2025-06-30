from unittest import mock
import pytest
from pytest_django.asserts import assertContains, assertTemplateUsed
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from core.types import ResultError

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


@pytest.mark.django_db
def test_criar_tipo_bem(admin_client):
    url = reverse_lazy("patrimonio:criar_tipo_bem")
    data = {"descricao": "Projetor Novo"}

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert TipoBem.objects.filter(descricao="Projetor Novo").exists()
    assertContains(response, "Projetor Novo")


@pytest.mark.django_db
def test_criar_tipo_bem_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_tipo_bem")
    response = client.post(url, {"descricao": "Cadeira"}, follow=True)

    assert response.status_code == 403
    assert not TipoBem.objects.filter(descricao="Cadeira").exists()


@pytest.mark.django_db
def test_editar_tipo_bem(admin_client):
    tipo = TipoBem.objects.create(descricao="Monitor Antigo")
    url = reverse_lazy("patrimonio:editar_tipo_bem", args=[tipo.pk])
    data = {"descricao": "Monitor LG"}

    response = admin_client.post(url, data, follow=True)

    tipo.refresh_from_db()
    assert tipo.descricao == "Monitor LG"
    assertContains(response, "Monitor LG")


@pytest.mark.django_db
def test_editar_tipo_bem_sem_permissao(client, test_user):
    client.force_login(test_user)

    tipo = TipoBem.objects.create(descricao="Switch")

    url = reverse_lazy("patrimonio:editar_tipo_bem", args=[tipo.pk])
    response = client.post(url, {"descricao": "Switch Novo"}, follow=True)

    tipo.refresh_from_db()
    assert tipo.descricao == "Switch"  # Não mudou
    assert response.status_code == 403


@pytest.mark.django_db
def test_remover_tipo_bem(admin_client):
    tipo = TipoBem.objects.create(descricao="Impressora")
    url = reverse_lazy("patrimonio:remover_tipo_bem", args=[tipo.pk])

    response = admin_client.post(url, follow=True)

    tipo.refresh_from_db()
    assert tipo.removido_em is not None


@pytest.mark.django_db
def test_remover_tipo_bem_sem_permissao(client, test_user):
    client.force_login(test_user)

    tipo = TipoBem.objects.create(descricao="Projetor Epson")

    url = reverse_lazy("patrimonio:remover_tipo_bem", args=[tipo.pk])
    response = client.post(url, follow=True)

    tipo.refresh_from_db()
    assert tipo.removido_em is None
    assert response.status_code == 403
