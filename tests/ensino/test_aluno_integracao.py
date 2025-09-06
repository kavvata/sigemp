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

from ensino.domain.entities import (
    AlunoEntity,
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
)
from ensino.models import Aluno, Campus, Curso, FormaSelecao

from pprint import pprint as print


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def campus(db):
    entity = CampusEntity(id=1, sigla="PNG", nome="Paranaguá")
    model, _criado = Campus.objects.get_or_create(
        entity.to_dict(
            [
                "timestamps",
                "campus_sigla",
            ]
        )
    )
    yield model

    model.delete()


@pytest.fixture
def curso(campus):
    e = CursoEntity(
        sigla="TADS",
        nome="Técnologo em Análise e Desenvolvimento de Sistemas",
        campus_id=campus.id,
    )
    model, _criado = Curso.objects.get_or_create(
        **e.to_dict(["timestamps", "campus_sigla"])
    )
    yield model

    model.delete()


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
def aluno_entity(curso, forma_selecao):
    return AlunoEntity(
        nome="Kawata",
        cpf="12345678900",
        email="kawata@ifpr.edu.br",
        matricula="2020001",
        telefone="41999990001",
        forma_selecao_id=1,
        curso_id=1,
    )


@pytest.fixture
def aluno(curso, forma_selecao):
    entity = AlunoEntity(
        id=1,
        nome="João da Silva",
        cpf="12345678901",
        email="joao.silva@ifpr.edu.br",
        matricula="2025001",
        telefone="41999990001",
        forma_selecao_id=forma_selecao.id,
        curso_id=curso.id,
    )

    model, _criado = Aluno.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def lista_alunos(curso, forma_selecao):
    lista_entities = [
        AlunoEntity(
            id=1,
            nome="João da Silva",
            cpf="12345678901",
            email="joao.silva@ifpr.edu.br",
            matricula="2025001",
            telefone="41999990001",
            forma_selecao_id=forma_selecao.id,
            curso_id=curso.id,
        ),
        AlunoEntity(
            id=2,
            nome="Ana Pereira",
            nome_responsavel="Carlos Pereira",
            cpf="98765432100",
            email="ana.pereira@ifpr.edu.br",
            matricula="2025002",
            telefone="41999990002",
            forma_selecao_id=forma_selecao.id,
            curso_id=curso.id,
        ),
        AlunoEntity(
            id=3,
            nome="Lucas Andrade",
            nome_responsavel="Fernanda Andrade",
            cpf="45678912300",
            email="lucas.andrade@ifpr.edu.br",
            matricula="2025003",
            telefone="41999990003",
            forma_selecao_id=forma_selecao.id,
            curso_id=curso.id,
        ),
        AlunoEntity(
            id=4,
            nome="Beatriz Costa",
            cpf="32165498700",
            email="beatriz.costa@ifpr.edu.br",
            matricula="2025004",
            telefone="41999990004",
            forma_selecao_id=forma_selecao.id,
            curso_id=curso.id,
        ),
        AlunoEntity(
            id=5,
            nome="Marcos Oliveira",
            cpf="15975348620",
            email="marcos.oliveira@ifpr.edu.br",
            matricula="2025005",
            telefone="41999990005",
            forma_selecao_id=forma_selecao.id,
            curso_id=curso.id,
        ),
    ]
    lista_models = [
        Aluno.objects.get_or_create(
            **e.to_dict(
                [
                    "timestamps",
                    "id",
                ]
            )
        )[0]
        for e in lista_entities
    ]

    yield lista_models

    for model in lista_models:
        model.delete()


@pytest.mark.django_db
def test_listar_alunos(lista_alunos, admin_client):
    response = admin_client.get(reverse_lazy("ensino:listar_alunos"))

    for aluno in [aluno.nome for aluno in lista_alunos]:
        assertContains(response, aluno)

    assertTemplateUsed(response, "ensino/aluno/aluno_list.html")


@pytest.mark.django_db
def test_listar_aluno_sem_permissao(client, test_user):
    client.force_login(test_user)

    url = reverse_lazy("ensino:listar_alunos")
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_criar_aluno(admin_client, aluno_entity: AlunoEntity):
    url = reverse_lazy("ensino:criar_aluno")

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    data = aluno_entity.to_dict(exclude=["timestamps", "id"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    assert Aluno.objects.filter(matricula=aluno_entity.matricula).exists()
    assertContains(response, aluno_entity.matricula)
    assertTemplateUsed(response, "ensino/aluno/aluno_list.html")


@pytest.mark.django_db
def test_criar_aluno_sem_permissao(client, test_user, aluno_entity: AlunoEntity):
    client.force_login(test_user)

    url = reverse_lazy("ensino:criar_aluno")

    response = client.get(url)

    assert response.status_code == 403

    data = aluno_entity.to_dict(exclude=["timestamps", "id"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = client.post(url, data, follow=True)
    print(response)
    print(response.text)

    assert response.status_code == 403
    assert not Aluno.objects.filter(matricula=aluno_entity.matricula).exists()
    assertTemplateNotUsed(response, "ensino/aluno/aluno_form.html")


@pytest.mark.django_db
def test_nao_pode_cadastrar_aluno_matricula_repetida(
    admin_client, aluno: Aluno, aluno_entity: AlunoEntity
):
    url = reverse_lazy("ensino:criar_aluno")

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    aluno_entity.matricula = aluno.matricula

    data = aluno_entity.to_dict(exclude=["timestamps", "id"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert Aluno.objects.filter(
        matricula=aluno.matricula,
        nome=aluno.nome,
    ).exists()
    assert not Aluno.objects.filter(
        matricula=aluno_entity.matricula,
        nome=aluno_entity.nome,
    ).exists()


@pytest.mark.django_db
def test_nao_pode_cadastrar_aluno_cpf_repetido(
    admin_client, aluno: Aluno, aluno_entity: AlunoEntity
):
    url = reverse_lazy("ensino:criar_aluno")

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    aluno_entity.cpf = aluno.cpf

    data = aluno_entity.to_dict(exclude=["timestamps", "id"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert Aluno.objects.filter(
        cpf=aluno.cpf,
        nome=aluno.nome,
    ).exists()
    assert not Aluno.objects.filter(
        cpf=aluno_entity.cpf,
        nome=aluno_entity.nome,
    ).exists()


@pytest.mark.django_db
def test_nao_pode_cadastrar_aluno_email_repetido(
    admin_client, aluno: Aluno, aluno_entity: AlunoEntity
):
    url = reverse_lazy("ensino:criar_aluno")

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    aluno_entity.email = aluno.email

    data = aluno_entity.to_dict(exclude=["timestamps", "id"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert Aluno.objects.filter(
        email=aluno.email,
        nome=aluno.nome,
    ).exists()
    assert not Aluno.objects.filter(
        email=aluno_entity.email,
        nome=aluno_entity.nome,
    ).exists()


@pytest.mark.django_db
def test_editar_aluno(admin_client, aluno: Aluno, aluno_entity: AlunoEntity):
    url = reverse_lazy("ensino:editar_aluno", args=[aluno.pk])

    response = admin_client.get(url)

    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    original = aluno.nome
    aluno_entity.id = aluno.id
    aluno_entity.nome = "Outro Nome"
    update_data = aluno_entity.to_dict(exclude=["timestamps"])
    update_data["curso"] = update_data.pop("curso_id")
    update_data["forma_selecao"] = update_data.pop("forma_selecao_id")
    update_data["nome_responsavel"] = ""

    response = admin_client.post(url, update_data, follow=True)

    aluno.refresh_from_db()
    assert aluno.nome == aluno_entity.nome
    assertContains(response, aluno_entity.nome)
    assertNotContains(response, original)
    assertTemplateUsed(response, "ensino/aluno/aluno_list.html")


@pytest.mark.django_db
def test_editar_aluno_sem_permissao(
    client, test_user, aluno, aluno_entity: AlunoEntity
):
    client.force_login(test_user)

    url = reverse_lazy("ensino:editar_aluno", args=[aluno.pk])

    response = client.get(url)

    assert response.status_code == 403

    original = aluno.email

    aluno_entity.id = aluno.id
    aluno_entity.email = "outro@email.com"

    update_data = aluno_entity.to_dict(exclude=["timestamps"])
    update_data["curso"] = update_data.pop("curso_id")
    update_data["forma_selecao"] = update_data.pop("forma_selecao_id")
    update_data["nome_responsavel"] = ""

    response = client.post(url, update_data, follow=True)

    assertTemplateNotUsed(response, "ensino/aluno/aluno_list.html")
    aluno.refresh_from_db()
    assert aluno.email == original
    assert not aluno.email == aluno_entity


@pytest.mark.django_db
def test_nao_pode_editar_aluno_matricula_repetida(
    admin_client, aluno: Aluno, lista_alunos: list[Aluno]
):
    url = reverse_lazy("ensino:editar_aluno", args=[aluno.pk])

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    aluno.matricula = lista_alunos[1].matricula

    data = aluno.to_dict(exclude=["timestamps"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert (
        Aluno.objects.filter(
            matricula=aluno.matricula,
            id=aluno.id,
        ).count()
        == 1
    )
    assert (
        not Aluno.objects.filter(
            matricula=aluno.matricula,
            id=aluno.id,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_nao_pode_editar_aluno_cpf_repetido(
    admin_client, aluno: Aluno, lista_alunos: list[Aluno]
):
    url = reverse_lazy("ensino:editar_aluno", args=[aluno.pk])

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    aluno.cpf = lista_alunos[1].cpf

    data = aluno.to_dict(exclude=["timestamps"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert (
        Aluno.objects.filter(
            cpf=aluno.cpf,
            id=aluno.id,
        ).count()
        == 1
    )
    assert (
        not Aluno.objects.filter(
            cpf=aluno.cpf,
            id=aluno.id,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_nao_pode_editar_aluno_email_repetido(
    admin_client, aluno: Aluno, lista_alunos: list[Aluno]
):
    url = reverse_lazy("ensino:editar_aluno", args=[aluno.pk])

    response = admin_client.get(url)
    assertTemplateUsed(response, "ensino/aluno/aluno_form.html")

    assert response.status_code == 200

    aluno.email = lista_alunos[1].email

    data = aluno.to_dict(exclude=["timestamps"])
    data["curso"] = data.pop("curso_id")
    data["forma_selecao"] = data.pop("forma_selecao_id")
    data["nome_responsavel"] = ""

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 403
    assert (
        Aluno.objects.filter(
            email=aluno.email,
            id=aluno.id,
        ).count()
        == 1
    )
    assert (
        not Aluno.objects.filter(
            email=aluno.email,
            id=aluno.id,
        ).count()
        == 1
    )


@pytest.mark.django_db
def test_remover_aluno(admin_client, aluno):
    url = reverse_lazy("ensino:remover_aluno", args=[aluno.pk])

    response = admin_client.post(url, follow=True)

    aluno.refresh_from_db()

    assert response.status_code == 200
    assert aluno.removido_em is not None

    response = admin_client.get(reverse_lazy("ensino:listar_alunos"))
    assertNotContains(response, aluno.nome)


@pytest.mark.django_db
def test_remover_aluno_sem_permissao(client, test_user, aluno):
    client.force_login(test_user)

    url = reverse_lazy("ensino:remover_aluno", args=[aluno.pk])
    response = client.post(url, follow=True)

    aluno.refresh_from_db()
    assert aluno.removido_em is None
    assert response.status_code == 403
