import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from patrimonio.domain.entities import BemEntity
from patrimonio.models import Bem


@pytest.fixture
def bem_entity():
    return BemEntity(
        patrimonio="000.000.000.000",
        descricao="Projetor Epson X1000",
        tipo_id=1,
        grau_fragilidade_id=2,
        estado_conservacao_id=1,
        marca_modelo_id=1,
    )


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture()
def bens(db):
    # TODO: realizar cadastros auxiliares
    bens_dict = [
        BemEntity(
            patrimonio="000.000.000.000",
            descricao="Projetor Epson X1000",
            tipo_id=1,
            grau_fragilidade_id=2,
            estado_conservacao_id=1,
            marca_modelo_id=1,
        ),
        BemEntity(
            patrimonio="000.000.000.001",
            descricao="Notebook Dell Latitude",
            tipo_id=2,
            grau_fragilidade_id=1,
            estado_conservacao_id=2,
            marca_modelo_id=2,
        ),
        BemEntity(
            patrimonio="000.000.000.002",
            descricao="Centrífuga de bancada",
            tipo_id=3,
            grau_fragilidade_id=3,
            estado_conservacao_id=3,
            marca_modelo_id=3,
        ),
    ]
    bens_models = [Bem.objects.get_or_create(bem.to_dict())[0] for bem in bens_dict]

    yield bens_models

    Bem.objects.filter(descricao__in=[b.descricao for b in bens_dict]).delete()


@pytest.fixture()
def bem(db):
    entity = BemEntity(
        id=1,
        patrimonio="000.000.000.000",
        descricao="Projetor Epson X1000",
        tipo_id=1,
        grau_fragilidade_id=2,
        estado_conservacao_id=1,
        marca_modelo_id=1,
    )
    model, _criado = Bem.objects.get_or_create(entity.to_dict())
    yield model

    model.delete()


@pytest.mark.django_db
def test_listar_bens(bens, admin_client):
    response = admin_client.get(reverse_lazy("patrimonio:listar_bens"))

    for bem in [bem.patrimonio for bem in bens]:
        assertContains(response, bem)

    assertTemplateUsed("patrimonio/bem_list.html")


@pytest.mark.django_db
def test_listar_bem_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:listar_bens")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_bem(admin_client, bem_entity: BemEntity):
    url = reverse_lazy("patrimonio:criar_bem")

    response = admin_client.get(url)

    assert response.status_code == 200

    data = bem_entity.to_dict()

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert Bem.objects.filter(descricao=data.descricao, nivel=data.nivel).exists()
    assertContains(response, data.descricao)
    assertTemplateUsed("patrimonio/bem_form.html")


@pytest.mark.django_db
def test_criar_bem_sem_permissao(client, test_user, bem_entity: BemEntity):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_bem")

    response = client.get(url)

    assert response.status_code == 403

    data = bem_entity.to_dict()

    response = client.post(url, data, follow=True)

    assert response.status_code == 403
    assert not Bem.objects.filter(patrimonio=bem_entity.patrimonio).exists()
    assertTemplateNotUsed("patrimonio/bem_form.html")


@pytest.mark.django_db
def test_editar_bem(admin_client, bem, bem_entity: BemEntity):
    url = reverse_lazy("patrimonio:editar_bem", args=[bem.pk])

    response = admin_client.get(url)

    assert response.status_code == 200

    original = bem.descricao
    bem_entity.descricao = "Outro Projetor"
    update_data = bem_entity.to_dict()

    response = admin_client.post(url, update_data, follow=True)

    bem.refresh_from_db()
    assert bem.descricao == bem_entity.descricao
    assertContains(response, bem_entity.descricao)
    assertNotContains(response, original)
    assertTemplateUsed("patrimonio/bem_form.html")


@pytest.mark.django_db
def test_editar_bem_sem_permissao(client, test_user, bem, bem_entity: BemEntity):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:editar_bem", args=[bem.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = bem.descricao

    bem_entity.descricao = "Outro Projetor"
    update_data = bem_entity.to_dict()

    response = client.post(url, update_data, follow=True)

    bem.refresh_from_db()
    assert bem.descricao == original
    assert response.status_code == 403
    assertTemplateNotUsed("patrimonio/bem_form.html")


@pytest.mark.django_db
def test_nao_pode_repetir_patrimonio(client, test_user, bem, bem_entity: BemEntity):
    raise NotImplementedError


@pytest.mark.django_db
def test_remover_bem(admin_client, bem):
    url = reverse_lazy("patrimonio:remover_bem", args=[bem.pk])

    response = admin_client.post(url, follow=True)

    bem.refresh_from_db()

    assert response.status_code == 200
    assert bem.removido_em is not None

    response = admin_client.get(reverse_lazy("patrimonio:listar_bens"))
    assertNotContains(response, bem.descricao)


@pytest.mark.django_db
def test_remover_bem_sem_permissao(client, test_user, bem):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:remover_bem", args=[bem.pk])
    response = client.post(url, follow=True)

    bem.refresh_from_db()
    assert bem.removido_em is None
    assert response.status_code == 403
