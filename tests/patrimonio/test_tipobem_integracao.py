import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from patrimonio.models import TipoBem


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture()
def tipos_de_bem(db):
    tipos_de_bem = [
        {"descricao": "Projetor"},
        {"descricao": "Notebook Dell"},
        {"descricao": "Frasco laboratorio"},
    ]
    tipos_de_bem_models = [
        TipoBem.objects.get_or_create(descricao=tp["descricao"])[0]
        for tp in tipos_de_bem
    ]

    yield tipos_de_bem_models

    TipoBem.objects.filter(
        descricao__in=[tp["descricao"] for tp in tipos_de_bem]
    ).delete()


@pytest.fixture
def tipo_bem(db):
    tipo_dict = {"descricao": "Projetor"}
    model, _created = TipoBem.objects.get_or_create(descricao=tipo_dict["descricao"])

    yield model

    model.delete()


@pytest.mark.django_db
def test_listar_tipos_bem(tipos_de_bem, admin_client):
    url = reverse_lazy("patrimonio:listar_tipos_bem")
    response = admin_client.get(url)

    for tipo in [tipo.descricao for tipo in tipos_de_bem]:
        assertContains(response, tipo)

    assert response.status_code == 200
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

    response = admin_client.get(url)

    assert response.status_code == 200

    data = {"descricao": "Projetor Novo"}

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert TipoBem.objects.filter(descricao="Projetor Novo").exists()
    assertContains(response, "Projetor Novo")
    assertTemplateUsed("patrimonio/tipo_bem_form.html")


@pytest.mark.django_db
def test_criar_tipo_bem_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_tipo_bem")

    response = client.get(url)

    assert response.status_code == 403

    response = client.post(url, {"descricao": "Cadeira"}, follow=True)

    assert response.status_code == 403
    assert not TipoBem.objects.filter(descricao="Cadeira").exists()
    assertTemplateNotUsed("patrimonio/tipo_bem_form.html")


@pytest.mark.django_db
def test_editar_tipo_bem(admin_client, tipo_bem):
    url = reverse_lazy("patrimonio:editar_tipo_bem", args=[tipo_bem.pk])
    data = {"descricao": "Monitor LG"}

    response = admin_client.get(url)

    assert response.status_code == 200

    response = admin_client.post(url, data, follow=True)

    tipo_bem.refresh_from_db()
    assert response.status_code == 200
    assert tipo_bem.descricao == data["descricao"]
    assertContains(response, data["descricao"])
    assertTemplateUsed("patrimonio/tipo_bem_form.html")


@pytest.mark.django_db
def test_editar_tipo_bem_sem_permissao(client, test_user, tipo_bem):
    client.force_login(test_user)

    original = tipo_bem.descricao

    url = reverse_lazy("patrimonio:editar_tipo_bem", args=[tipo_bem.pk])

    response = client.get(url)

    assert response.status_code == 403

    response = client.post(url, {"descricao": "Switch Novo"}, follow=True)

    tipo_bem.refresh_from_db()
    assert tipo_bem.descricao == original
    assert response.status_code == 403
    assertTemplateNotUsed("patrimonio/tipo_bem_form.html")


@pytest.mark.django_db
def test_remover_tipo_bem(admin_client, tipo_bem):
    url = reverse_lazy("patrimonio:remover_tipo_bem", args=[tipo_bem.pk])

    response = admin_client.post(url, follow=True)

    assert response.status_code == 200
    tipo_bem.refresh_from_db()
    assert tipo_bem.removido_em is not None

    response = admin_client.get(reverse_lazy("patrimonio:listar_tipos_bem"))
    assertNotContains(response, tipo_bem.descricao)


@pytest.mark.django_db
def test_remover_tipo_bem_sem_permissao(client, test_user, tipo_bem):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:remover_tipo_bem", args=[tipo_bem.pk])
    response = client.post(url, follow=True)

    tipo_bem.refresh_from_db()
    assert tipo_bem.removido_em is None
    assert response.status_code == 403
