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
from patrimonio.models import (
    Bem,
    TipoBem,
    GrauFragilidade,
    EstadoConservacao,
    MarcaModelo,
)


@pytest.fixture
def bem_entity(
    lista_grau_fragilidade,
    tipos_de_bem,
    estados_conservacao,
    marcas_modelos,
):
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
def bens(db, lista_grau_fragilidade, tipos_de_bem, estados_conservacao, marcas_modelos):
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

    assertTemplateUsed(response, "patrimonio/bem/bem_list.html")


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
    assertTemplateUsed(response, "patrimonio/bem/bem_form.html")

    assert response.status_code == 200

    data = bem_entity.to_dict(exclude=["timestamps", "id"])
    data["tipo"] = data.pop("tipo_id")
    data["estado_conservacao"] = data.pop("estado_conservacao_id")
    data["grau_fragilidade"] = data.pop("grau_fragilidade_id")
    data["marca_modelo"] = data.pop("marca_modelo_id")

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert Bem.objects.filter(patrimonio=bem_entity.patrimonio).exists()
    assertContains(response, bem_entity.patrimonio)
    assertTemplateUsed(response, "patrimonio/bem/bem_list.html")


@pytest.mark.django_db
def test_criar_bem_sem_permissao(client, test_user, bem_entity: BemEntity):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:criar_bem")

    response = client.get(url)

    assert response.status_code == 403

    data = bem_entity.to_dict(exclude=["timestamps", "id"])
    data["tipo"] = data.pop("tipo_id")
    data["estado_conservacao"] = data.pop("estado_conservacao_id")
    data["grau_fragilidade"] = data.pop("grau_fragilidade_id")
    data["marca_modelo"] = data.pop("marca_modelo_id")

    response = client.post(url, data, follow=True)

    assert response.status_code == 403
    assert not Bem.objects.filter(patrimonio=bem_entity.patrimonio).exists()
    assertTemplateNotUsed(response, "patrimonio/bem/bem_form.html")


@pytest.mark.django_db
def test_editar_bem(admin_client, bem, bem_entity: BemEntity):
    url = reverse_lazy("patrimonio:editar_bem", args=[bem.pk])

    response = admin_client.get(url)

    assertTemplateUsed(response, "patrimonio/bem/bem_form.html")

    assert response.status_code == 200

    original = bem.descricao
    bem_entity.id = bem.id
    bem_entity.descricao = "Outro Projetor"
    update_data = bem_entity.to_dict(exclude=["timestamps"])
    update_data["tipo"] = update_data.pop("tipo_id")
    update_data["estado_conservacao"] = update_data.pop("estado_conservacao_id")
    update_data["grau_fragilidade"] = update_data.pop("grau_fragilidade_id")
    update_data["marca_modelo"] = update_data.pop("marca_modelo_id")

    response = admin_client.post(url, update_data, follow=True)

    bem.refresh_from_db()
    assert bem.descricao == bem_entity.descricao
    assertContains(response, bem_entity.descricao)
    assertNotContains(response, original)
    assertTemplateUsed(response, "patrimonio/bem/bem_list.html")


@pytest.mark.django_db
def test_editar_bem_sem_permissao(client, test_user, bem, bem_entity: BemEntity):
    client.force_login(test_user)

    url = reverse_lazy("patrimonio:editar_bem", args=[bem.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = bem.descricao

    bem_entity.id = bem.id
    bem_entity.descricao = "Outro Projetor"

    update_data = bem_entity.to_dict(exclude=["timestamps"])
    update_data["tipo"] = update_data.pop("tipo_id")
    update_data["estado_conservacao"] = update_data.pop("estado_conservacao_id")
    update_data["grau_fragilidade"] = update_data.pop("grau_fragilidade_id")
    update_data["marca_modelo"] = update_data.pop("marca_modelo_id")

    response = client.post(url, update_data, follow=True)

    assertTemplateNotUsed(response, "patrimonio/bem/bem_list.html")
    bem.refresh_from_db()
    assert bem.descricao == original


@pytest.mark.django_db
def test_nao_pode_repetir_patrimonio(admin_client, bem, bem_entity: BemEntity):
    url = reverse_lazy("patrimonio:criar_bem")

    response = admin_client.get(url)
    assertTemplateUsed(response, "patrimonio/bem/bem_form.html")

    assert response.status_code == 200

    bem_entity.patrimonio = bem.patrimonio

    data = bem_entity.to_dict(exclude=["timestamps", "id"])
    data["tipo"] = data.pop("tipo_id")
    data["estado_conservacao"] = data.pop("estado_conservacao_id")
    data["grau_fragilidade"] = data.pop("grau_fragilidade_id")
    data["marca_modelo"] = data.pop("marca_modelo_id")

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert Bem.objects.filter(patrimonio=bem_entity.patrimonio, id=bem.id).exists()


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
