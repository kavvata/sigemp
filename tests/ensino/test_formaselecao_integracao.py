from datetime import datetime, timedelta
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from ensino.domain.entities import FormaSelecaoEntity
from ensino.models import FormaSelecao


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def forma_selecao_entity():
    base_date = datetime(2020, 1, 1)
    return FormaSelecaoEntity(
        descricao="Edital N°01/2020",
        periodo_inicio=base_date,
        periodo_fim=base_date + timedelta(days=180),
    )


@pytest.fixture
def forma_selecao(db):
    base_date = datetime(2020, 1, 1)
    entity = FormaSelecaoEntity(
        descricao="Edital N°01/2020",
        periodo_inicio=base_date,
        periodo_fim=base_date + timedelta(days=180),
    )
    model, _criado = FormaSelecao.objects.get_or_create(entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def lista_formas_selecao(db):
    base_date = datetime(2020, 1, 1)
    lista_entities = [
        FormaSelecaoEntity(
            descricao="Edital N°01/2020",
            periodo_inicio=base_date,
            periodo_fim=base_date + timedelta(days=180),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°02/2020",
            periodo_inicio=base_date + timedelta(days=200),
            periodo_fim=base_date + timedelta(days=365),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°03/2021",
            periodo_inicio=base_date.replace(year=2021, month=3, day=15),
            periodo_fim=base_date.replace(year=2021, month=9, day=15),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°04/2021",
            periodo_inicio=base_date.replace(year=2021, month=10, day=1),
            periodo_fim=base_date.replace(year=2022, month=3, day=1),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°05/2022",
            periodo_inicio=base_date.replace(year=2022, month=4, day=10),
            periodo_fim=base_date.replace(year=2023, month=4, day=10),
        ),
    ]

    formas_selecao_models = [
        FormaSelecao.objects.get_or_create(**e.to_dict())[0] for e in lista_entities
    ]
    yield formas_selecao_models

    FormaSelecao.objects.filter(
        descricao__in=[e.descricao for e in lista_entities]
    ).delete()


@pytest.mark.django_db
def test_listar_formas_selecao(lista_formas_selecao, admin_client):
    response = admin_client.get(reverse_lazy("ensino:listar_formas_selecao"))
    for descricao in [
        forma_selecao.descricao for forma_selecao in lista_formas_selecao
    ]:
        assertContains(response, descricao)

    assertTemplateUsed(response, "ensino/forma_selecao/formaselecao_list.html")


@pytest.mark.django_db
def test_nao_pode_listar_formas_selecao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("ensino:listar_formas_selecao")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_forma_selecao(admin_client, forma_selecao_entity: FormaSelecaoEntity):
    url = reverse_lazy("ensino:criar_forma_selecao")
    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/forma_selecao/formaselecao_form.html")

    assert response.status_code == 200

    form_data = forma_selecao_entity.to_dict(["timestamps", "id"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = admin_client.post(url, form_data, follow=True)

    assert response.status_code == 200
    assert FormaSelecao.objects.filter(
        descricao=forma_selecao_entity.descricao
    ).exists()
    assertContains(response, forma_selecao_entity.descricao)
    assertTemplateUsed(response, "ensino/forma_selecao/formaselecao_list.html")


@pytest.mark.django_db
def test_nao_pode_criar_forma_selecao(
    client, test_user, forma_selecao_entity: FormaSelecaoEntity
):
    client.force_login(test_user)

    url = reverse_lazy("ensino:criar_forma_selecao")

    response = client.get(url)

    assert response.status_code == 403

    form_data = forma_selecao_entity.to_dict(["timestamps", "id"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = client.post(url, form_data, follow=True)

    assert response.status_code == 403
    assert not FormaSelecao.objects.filter(
        descricao=forma_selecao_entity.descricao
    ).exists()
    assertTemplateNotUsed(response, "ensino/forma_selecao/formaselecao_form.html")


@pytest.mark.django_db
def test_editar_forma_selecao(
    admin_client, forma_selecao_entity: FormaSelecaoEntity, forma_selecao
):
    url = reverse_lazy("ensino:editar_forma_selecao", args=[forma_selecao.pk])

    response = admin_client.get(url)

    assertTemplateUsed(response, "ensino/forma_selecao/formaselecao_form.html")
    assert response.status_code == 200

    original = forma_selecao.descricao
    forma_selecao_entity.id = forma_selecao.id
    forma_selecao_entity.descricao = "Edital Número 01/2020"

    form_data = forma_selecao_entity.to_dict(exclude=["timestamps"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = admin_client.post(url, form_data, follow=True)
    forma_selecao.refresh_from_db()
    assert forma_selecao.descricao == forma_selecao_entity.descricao
    assertContains(response, forma_selecao_entity.descricao)
    assertTemplateUsed(response, "ensino/forma_selecao/formaselecao_list.html")


@pytest.mark.django_db
def test_nao_pode_editar_forma_selecao(
    client, test_user, forma_selecao_entity: FormaSelecaoEntity, forma_selecao
):
    client.force_login(test_user)
    url = reverse_lazy("ensino:editar_forma_selecao", args=[forma_selecao.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = forma_selecao.descricao

    forma_selecao_entity.id = forma_selecao.id
    forma_selecao_entity.descricao = "Edital Nº XXX/2025"

    form_data = forma_selecao_entity.to_dict(exclude=["timestamps"])
    form_data["periodo_inicio"] = form_data["periodo_inicio"].strftime("%Y-%m-%d")
    form_data["periodo_fim"] = form_data["periodo_fim"].strftime("%Y-%m-%d")

    response = client.post(url, form_data, follow=True)
    assertTemplateNotUsed(response, "ensino/forma_selecao/formaselecao_list.html")
    forma_selecao.refresh_from_db()
    assert forma_selecao.descricao == original


@pytest.mark.django_db
def test_remover_forma_selecao(admin_client, forma_selecao):
    url = reverse_lazy("ensino:remover_forma_selecao", args=[forma_selecao.pk])

    response = admin_client.post(url, follow=True)

    forma_selecao.refresh_from_db()

    assert response.status_code == 200
    assert forma_selecao.removido_em is not None

    response = admin_client.get(reverse_lazy("ensino:listar_formas_selecao"))
    assertNotContains(response, forma_selecao.descricao)


@pytest.mark.django_db
def test_nao_pode_remover_forma_selecao(client, test_user, forma_selecao):
    client.force_login(test_user)

    url = reverse_lazy("ensino:remover_forma_selecao", args=[forma_selecao.pk])
    response = client.post(url, follow=True)

    forma_selecao.refresh_from_db()
    assert forma_selecao.removido_em is None
    assert response.status_code == 403
