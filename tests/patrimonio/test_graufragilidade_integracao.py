import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from patrimonio.models import GrauFragilidade


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture()
def lista_grau_fragilidade(db):
    grau_fragilidade_dict = [
        {"descricao": "Péssimo", "nivel": 1},
        {"descricao": "Mau", "nivel": 2},
        {"descricao": "Médio", "nivel": 3},
        {"descricao": "Bom", "nivel": 4},
        {"descricao": "Excelente", "nivel": 5},
    ]
    grau_fragilidade_models = [
        GrauFragilidade.objects.get_or_create(
            descricao=ec["descricao"], nivel=ec["nivel"]
        )[0]
        for ec in grau_fragilidade_dict
    ]

    yield grau_fragilidade_models

    GrauFragilidade.objects.filter(
        descricao__in=[ec["descricao"] for ec in grau_fragilidade_dict]
    ).delete()


@pytest.fixture()
def grau_fragilidade(db):
    data = {"descricao": "Médio", "nivel": 3}
    model, _criado = GrauFragilidade.objects.get_or_create(
        descricao=data["descricao"], nivel=data["nivel"]
    )
    yield model

    model.delete()


@pytest.mark.django_db
def test_listar_grau_fragilidade(lista_grau_fragilidade, admin_client):
    response = admin_client.get(reverse_lazy("patrimonio:listar_grau_fragilidade"))

    for grau in [grau.descricao for grau in lista_grau_fragilidade]:
        assertContains(response, grau)

    assertTemplateUsed("patrimonio/grau_fragilidade_list.html")


@pytest.mark.django_db
def test_listar_grau_fragilidade_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:listar_grau_fragilidade")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_grau_fragilidade(admin_client):
    url = reverse_lazy("patrimonio:criar_grau_fragilidade")

    response = admin_client.get(url)

    assert response.status_code == 200

    data = {"descricao": "Médio", "nivel": 3}

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert GrauFragilidade.objects.filter(
        descricao=data["descricao"], nivel=data["nivel"]
    ).exists()
    assertContains(response, data["descricao"])
    assertTemplateUsed("patrimonio/grau_fragilidade_form.html")


@pytest.mark.django_db
def test_criar_grau_fragilidade_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_grau_fragilidade")

    response = client.get(url)

    assert response.status_code == 403

    data = {"descricao": "Médio", "nivel": 3}

    response = client.post(url, data, follow=True)

    assert response.status_code == 403
    assert not GrauFragilidade.objects.filter(descricao="Médio").exists()
    assertTemplateNotUsed("patrimonio/grau_fragilidade_form.html")


@pytest.mark.django_db
def test_editar_grau_fragilidade(admin_client, grau_fragilidade):
    url = reverse_lazy("patrimonio:editar_grau_fragilidade", args=[grau_fragilidade.pk])

    response = admin_client.get(url)

    assert response.status_code == 200

    original = grau_fragilidade.descricao
    update_data = {"descricao": "Moderado", "nivel": 3}

    response = admin_client.post(url, update_data, follow=True)

    grau_fragilidade.refresh_from_db()
    assert grau_fragilidade.descricao == update_data["descricao"]
    assertContains(response, update_data["descricao"])
    assertNotContains(response, original)
    assertTemplateUsed("patrimonio/grau_fragilidade_form.html")


@pytest.mark.django_db
def test_editar_grau_fragilidade_sem_permissao(client, test_user, grau_fragilidade):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:editar_grau_fragilidade", args=[grau_fragilidade.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = grau_fragilidade.descricao

    update_data = {"descricao": "Moderado", "nivel": 3}

    response = client.post(url, update_data, follow=True)

    grau_fragilidade.refresh_from_db()
    assert grau_fragilidade.descricao == original
    assert response.status_code == 403
    assertTemplateNotUsed("patrimonio/grau_fragilidade_form.html")


@pytest.mark.django_db
def test_remover_grau_fragilidade(admin_client, grau_fragilidade):
    url = reverse_lazy(
        "patrimonio:remover_grau_fragilidade", args=[grau_fragilidade.pk]
    )

    response = admin_client.post(url, follow=True)

    grau_fragilidade.refresh_from_db()

    assert response.status_code == 200
    assert grau_fragilidade.removido_em is not None

    response = admin_client.get(reverse_lazy("patrimonio:listar_grau_fragilidade"))
    assertNotContains(response, grau_fragilidade.descricao)


@pytest.mark.django_db
def test_remover_grau_fragilidade_sem_permissao(client, test_user, grau_fragilidade):
    client.force_login(test_user)

    url = reverse_lazy(
        "patrimonio:remover_grau_fragilidade", args=[grau_fragilidade.pk]
    )
    response = client.post(url, follow=True)

    grau_fragilidade.refresh_from_db()
    assert grau_fragilidade.removido_em is None
    assert response.status_code == 403
