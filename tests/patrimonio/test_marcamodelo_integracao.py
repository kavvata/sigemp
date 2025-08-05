import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from patrimonio.models import MarcaModelo


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture()
def marcas_modelos(db):
    marcas_modelos_dict = [
        {"marca": "Epson", "modelo": "PowerLite X49"},
        {"marca": "Dell", "modelo": "Latitude 5420"},
        {"marca": "Optika", "modelo": "B-150R"},
        {"marca": "Minipa", "modelo": "ET-1002"},
        {"marca": "Canon", "modelo": "EOS Rebel T7"},
    ]
    marcas_modelos_models = [
        MarcaModelo.objects.get_or_create(marca=mm["marca"], modelo=mm["modelo"])[0]
        for mm in marcas_modelos_dict
    ]

    yield marcas_modelos_models

    MarcaModelo.objects.filter(
        modelo__in=[mm["modelo"] for mm in marcas_modelos_dict],
    ).delete()


@pytest.fixture()
def marca_modelo(db):
    data = {"marca": "Epson", "modelo": "PowerLite X49"}
    model, _criado = MarcaModelo.objects.get_or_create(
        marca=data["marca"], modelo=data["modelo"]
    )
    yield model

    model.delete()


@pytest.mark.django_db
def test_listar_marcas_modelos(marcas_modelos, admin_client):
    response = admin_client.get(reverse_lazy("patrimonio:listar_marca_modelo"))

    for marca_modelo in [marca_modelo.marca for marca_modelo in marcas_modelos]:
        assertContains(response, marca_modelo)

    assertTemplateUsed("patrimonio/marca_modelo_list.html")


@pytest.mark.django_db
def test_listar_marca_modelo_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:listar_marca_modelo")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_marca_modelo(admin_client):
    url = reverse_lazy("patrimonio:criar_marca_modelo")

    response = admin_client.get(url)

    assert response.status_code == 200

    data = {"marca": "Epson", "modelo": "Outro Modelo"}

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert MarcaModelo.objects.filter(
        marca=data["marca"], modelo=data["modelo"]
    ).exists()
    assertContains(response, data["marca"])
    assertTemplateUsed("patrimonio/marca_modelo_form.html")


@pytest.mark.django_db
def test_criar_marca_modelo_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_marca_modelo")

    response = client.get(url)

    assert response.status_code == 403

    data = {"marca": "Epson", "modelo": "PowerLite X49"}

    response = client.post(url, data, follow=True)

    assert response.status_code == 403
    assert not MarcaModelo.objects.filter(marca="Médio").exists()
    assertTemplateNotUsed("patrimonio/marca_modelo_form.html")


@pytest.mark.django_db
def test_editar_marca_modelo(admin_client, marca_modelo):
    url = reverse_lazy("patrimonio:editar_marca_modelo", args=[marca_modelo.pk])

    response = admin_client.get(url)

    assert response.status_code == 200

    original = marca_modelo.modelo
    update_data = {"marca": "Epson", "modelo": "Outro Modelo"}

    response = admin_client.post(url, update_data, follow=True)

    marca_modelo.refresh_from_db()
    assert marca_modelo.modelo == update_data["modelo"]
    assertContains(response, update_data["modelo"])
    assertNotContains(response, original)
    assertTemplateUsed("patrimonio/marca_modelo_form.html")


@pytest.mark.django_db
def test_editar_marca_modelo_sem_permissao(client, test_user, marca_modelo):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:editar_marca_modelo", args=[marca_modelo.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = marca_modelo.modelo

    update_data = {"marca": "Epson", "modelo": "Outro Modelo"}

    response = client.post(url, update_data, follow=True)

    marca_modelo.refresh_from_db()
    assert marca_modelo.modelo == original
    assert response.status_code == 403
    assertTemplateNotUsed("patrimonio/marca_modelo_form.html")


@pytest.mark.django_db
def test_remover_marca_modelo(admin_client, marca_modelo):
    url = reverse_lazy("patrimonio:remover_marca_modelo", args=[marca_modelo.pk])

    response = admin_client.post(url, follow=True)

    marca_modelo.refresh_from_db()

    assert response.status_code == 200
    assert marca_modelo.removido_em is not None

    response = admin_client.get(reverse_lazy("patrimonio:listar_marca_modelo"))
    assertNotContains(response, marca_modelo.marca)


@pytest.mark.django_db
def test_remover_marca_modelo_sem_permissao(client, test_user, marca_modelo):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:remover_marca_modelo", args=[marca_modelo.pk])
    response = client.post(url, follow=True)

    marca_modelo.refresh_from_db()
    assert marca_modelo.removido_em is None
    assert response.status_code == 403
