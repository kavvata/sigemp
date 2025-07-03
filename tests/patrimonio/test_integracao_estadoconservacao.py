import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from patrimonio.models import EstadoConservacao


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture()
def estados_conservacao(db):
    estados_conservacao_dict = [
        {"descricao": "Péssimo", "nivel": 1},
        {"descricao": "Mau", "nivel": 2},
        {"descricao": "Médio", "nivel": 3},
        {"descricao": "Bom", "nivel": 4},
        {"descricao": "Excelente", "nivel": 5},
    ]
    estados_conservacao_models = [
        EstadoConservacao.objects.get_or_create(
            descricao=ec["descricao"], nivel=ec["nivel"]
        )[0]
        for ec in estados_conservacao_dict
    ]

    yield estados_conservacao_models

    EstadoConservacao.objects.filter(
        descricao__in=[ec["descricao"] for ec in estados_conservacao_dict]
    ).delete()


@pytest.fixture()
def estado_conservacao(db):
    data = {"descricao": "Médio", "nivel": 3}
    model, _criado = EstadoConservacao.objects.get_or_create(
        descricao=data["descricao"], nivel=data["nivel"]
    )
    yield model

    model.delete()


@pytest.mark.django_db
def test_listar_estados_conservacao(estados_conservacao, admin_client):
    response = admin_client.get(reverse_lazy("patrimonio:listar_estados_conservacao"))

    for estado in [estado.descricao for estado in estados_conservacao]:
        assertContains(response, estado)

    assertTemplateUsed("patrimonio/estado_conservacao_list.html")


@pytest.mark.django_db
def test_listar_estado_conservacao_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:estados_conservacao")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_estado_conservacao(admin_client):
    url = reverse_lazy("patrimonio:criar_estado_conservacao")

    response = admin_client.get(url)

    assert response.status_code == 200

    data = {"descricao": "Médio", "nivel": 3}

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert EstadoConservacao.objects.filter(
        descricao=data["descricao"], nivel=data["nivel"]
    ).exists()
    assertContains(response, "Projetor Novo")
    assertTemplateUsed("patrimonio/estado_conservacao_form.html")


@pytest.mark.django_db
def test_criar_estado_conservacao_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_estado_conservacao")

    response = client.get(url)

    assert response.status_code == 403

    data = {"descricao": "Médio", "nivel": 3}

    response = client.post(url, data, follow=True)

    assert response.status_code == 403
    assert not EstadoConservacao.objects.filter(descricao="Médio").exists()
    assertTemplateNotUsed("patrimonio/estado_conservacao_form.html")


@pytest.mark.django_db
def test_editar_estado_conservacao(admin_client, estado_conservacao):
    url = reverse_lazy(
        "patrimonio:editar_estado_conservacao", args=[estado_conservacao.pk]
    )

    response = admin_client.get(url)

    assert response.status_code == 200

    original = estado_conservacao.descricao
    update_data = {"descricao": "Moderado", "nivel": 3}

    response = admin_client.post(url, update_data, follow=True)

    estado_conservacao.refresh_from_db()
    assert estado_conservacao.descricao == update_data["descricao"]
    assertContains(response, update_data["descricao"])
    assertNotContains(response, original)
    assertTemplateUsed("patrimonio/estado_conservacao_form.html")


@pytest.mark.django_db
def test_editar_estado_conservacao_sem_permissao(client, test_user, estado_conservacao):
    client.force_login(test_user)

    url = reverse_lazy(
        "patrimonio:editar_estado_conservacao", args=[estado_conservacao.pk]
    )

    response = client.get(url)

    assert response.status_code == 403

    original = estado_conservacao.descricao

    update_data = {"descricao": "Moderado", "nivel": 3}

    response = client.post(url, update_data, follow=True)

    estado_conservacao.refresh_from_db()
    assert estado_conservacao.descricao == original
    assert response.status_code == 403
    assertTemplateNotUsed("patrimonio/estado_conservacao_form.html")


@pytest.mark.django_db
def test_remover_estado_conservacao(admin_client, estado_conservacao):
    url = reverse_lazy(
        "patrimonio:remover_estado_conservacao", args=[estado_conservacao.pk]
    )

    response = admin_client.post(url, follow=True)

    estado_conservacao.refresh_from_db()

    assert response.status_code == 200
    assert estado_conservacao.removido_em is not None

    response = admin_client.get(reverse_lazy("patrimonio:listar_estados_conservacao"))
    assertNotContains(response, estado_conservacao.descricao)


@pytest.mark.django_db
def test_remover_estado_conservacao_sem_permissao(
    client, test_user, estado_conservacao
):
    client.force_login(test_user)

    url = reverse_lazy(
        "patrimonio:remover_estado_conservacao", args=[estado_conservacao.pk]
    )
    response = client.post(url, follow=True)

    estado_conservacao.refresh_from_db()
    assert estado_conservacao.removido_em is None
    assert response.status_code == 403

    assertNotContains(response, estado_conservacao.descricao)
