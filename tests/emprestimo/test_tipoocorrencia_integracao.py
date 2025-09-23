import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from ensino.domain.entities import TipoOcorrenciaEntity
from ensino.models import TipoOcorrencia


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def tipo_ocorrencia_entity():
    return TipoOcorrenciaEntity(id=1, descricao="Perda")


@pytest.fixture
def tipo_ocorrencia(db):
    entity = TipoOcorrenciaEntity(id=1, descricao="Perda")
    model, _criado = TipoOcorrencia.objects.get_or_create(entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def lista_tipos_ocorrencia(db):
    lista_entities = [
        TipoOcorrenciaEntity(id=1, descricao="Perda"),
        TipoOcorrenciaEntity(id=2, descricao="Roubo"),
        TipoOcorrenciaEntity(id=3, descricao="Extravio"),
        TipoOcorrenciaEntity(id=4, descricao="Dano"),
    ]

    tipos_ocorrencia_models = [
        TipoOcorrencia.objects.get_or_create(**e.to_dict())[0] for e in lista_entities
    ]
    yield tipos_ocorrencia_models

    TipoOcorrencia.objects.filter(
        descricao__in=[e.descricao for e in lista_entities]
    ).delete()


@pytest.mark.django_db
def test_listar_tipos_ocorrencia(lista_tipos_ocorrencia, admin_client):
    response = admin_client.get(reverse_lazy("ensino:listar_tipos_ocorrencia"))
    for descricao in [
        tipo_ocorrencia.descricao for tipo_ocorrencia in lista_tipos_ocorrencia
    ]:
        assertContains(response, descricao)

    assertTemplateUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_list.html")


@pytest.mark.django_db
def test_nao_pode_listar_tipos_ocorrencia(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("ensino:listar_tipos_ocorrencia")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_tipo_ocorrencia(
    admin_client, tipo_ocorrencia_entity: TipoOcorrenciaEntity
):
    url = reverse_lazy("ensino:criar_tipo_ocorrencia")
    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_form.html")

    assert response.status_code == 200

    form_data = tipo_ocorrencia_entity.to_dict(["timestamps", "id"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = admin_client.post(url, form_data, follow=True)

    assert response.status_code == 200
    assert TipoOcorrencia.objects.filter(
        descricao=tipo_ocorrencia_entity.descricao
    ).exists()
    assertContains(response, tipo_ocorrencia_entity.descricao)
    assertTemplateUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_list.html")


@pytest.mark.django_db
def test_nao_pode_criar_tipo_ocorrencia(
    client, test_user, tipo_ocorrencia_entity: TipoOcorrenciaEntity
):
    client.force_login(test_user)

    url = reverse_lazy("ensino:criar_tipo_ocorrencia")

    response = client.get(url)

    assert response.status_code == 403

    form_data = tipo_ocorrencia_entity.to_dict(["timestamps", "id"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = client.post(url, form_data, follow=True)

    assert response.status_code == 403
    assert not TipoOcorrencia.objects.filter(
        descricao=tipo_ocorrencia_entity.descricao
    ).exists()
    assertTemplateNotUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_form.html")


@pytest.mark.django_db
def test_editar_tipo_ocorrencia(
    admin_client, tipo_ocorrencia_entity: TipoOcorrenciaEntity, tipo_ocorrencia
):
    url = reverse_lazy("ensino:editar_tipo_ocorrencia", args=[tipo_ocorrencia.pk])

    response = admin_client.get(url)

    assertTemplateUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_form.html")
    assert response.status_code == 200

    original = tipo_ocorrencia.descricao
    tipo_ocorrencia_entity.id = tipo_ocorrencia.id
    tipo_ocorrencia_entity.descricao = "Edital Número 01/2020"

    form_data = tipo_ocorrencia_entity.to_dict(exclude=["timestamps"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = admin_client.post(url, form_data, follow=True)
    tipo_ocorrencia.refresh_from_db()
    assert tipo_ocorrencia.descricao == tipo_ocorrencia_entity.descricao
    assertContains(response, tipo_ocorrencia_entity.descricao)
    assertTemplateUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_list.html")


@pytest.mark.django_db
def test_nao_pode_editar_tipo_ocorrencia(
    client, test_user, tipo_ocorrencia_entity: TipoOcorrenciaEntity, tipo_ocorrencia
):
    client.force_login(test_user)
    url = reverse_lazy("ensino:editar_tipo_ocorrencia", args=[tipo_ocorrencia.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = tipo_ocorrencia.descricao

    tipo_ocorrencia_entity.id = tipo_ocorrencia.id
    tipo_ocorrencia_entity.descricao = "Edital Nº XXX/2025"

    form_data = tipo_ocorrencia_entity.to_dict(exclude=["timestamps"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = client.post(url, form_data, follow=True)
    assertTemplateNotUsed(response, "ensino/tipo_ocorrencia/tiposocorrencia_list.html")
    tipo_ocorrencia.refresh_from_db()
    assert tipo_ocorrencia.descricao == original


@pytest.mark.django_db
def test_remover_tipo_ocorrencia(admin_client, tipo_ocorrencia):
    url = reverse_lazy("ensino:remover_tipo_ocorrencia", args=[tipo_ocorrencia.pk])

    response = admin_client.post(url, follow=True)

    tipo_ocorrencia.refresh_from_db()

    assert response.status_code == 200
    assert tipo_ocorrencia.removido_em is not None

    response = admin_client.get(reverse_lazy("ensino:listar_tipos_ocorrencia"))
    assertNotContains(response, tipo_ocorrencia.descricao)


@pytest.mark.django_db
def test_nao_pode_remover_tipo_ocorrencia(client, test_user, tipo_ocorrencia):
    client.force_login(test_user)

    url = reverse_lazy("ensino:remover_tipo_ocorrencia", args=[tipo_ocorrencia.pk])
    response = client.post(url, follow=True)

    tipo_ocorrencia.refresh_from_db()
    assert tipo_ocorrencia.removido_em is None
    assert response.status_code == 403
