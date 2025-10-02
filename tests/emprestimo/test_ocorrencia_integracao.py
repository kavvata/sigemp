from datetime import date
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateUsed,
    assertTemplateNotUsed,
)

from emprestimo.domain.entities import OcorrenciaEntity
from emprestimo.models import Ocorrencia

from tests.emprestimo.test_tipoocorrencia_integracao import lista_tipos_ocorrencia  # noqa: F401
from tests.emprestimo.test_emprestimo_integrcao import (
    emprestimo,  # noqa: F401  # pyright: ignore[reportUnusedImport]
    aluno,  # noqa: F401  # pyright: ignore[reportUnusedImport]
    lista_alunos,  # noqa: F401  # pyright: ignore[reportUnusedImport]
    lista_emprestimos_em_andamento,  # noqa: F401  # pyright: ignore[reportUnusedImport]
)


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def ocorrencia(db, emprestimo, lista_tipos_ocorrencia, test_user):
    entity = OcorrenciaEntity(
        id=1,
        data_ocorrencia=date(2025, 10, 1),
        emprestimo_id=emprestimo.id,
        tipo_id=lista_tipos_ocorrencia[0].id,
        tipo_descricao=lista_tipos_ocorrencia[0].descricao,
    )
    model, _criado = Ocorrencia.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def ocorrencia_cancelada(db, emprestimo, lista_tipos_ocorrencia, test_user):
    entity = OcorrenciaEntity(
        id=2,
        data_ocorrencia=date(2025, 10, 1),
        emprestimo_id=emprestimo.id,
        tipo_id=lista_tipos_ocorrencia[0].id,
        tipo_descricao=lista_tipos_ocorrencia[0].descricao,
        cancelado_em=date(2025, 10, 2),
        cancelado_por_id=test_user.id,
        motivo_cancelamento="Registro duplicado",
    )
    model, _criado = Ocorrencia.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def lista_ocorrencias(
    db, lista_emprestimos_em_andamento, lista_tipos_ocorrencia, test_user
):
    entities = []
    for i, (emprestimo, tipo_ocorrencia) in enumerate(
        zip(lista_emprestimos_em_andamento[:4], lista_tipos_ocorrencia[:4])
    ):
        entity = OcorrenciaEntity(
            id=i + 1,
            data_ocorrencia=date(2025, 10, 1) if i % 2 == 0 else date(2025, 10, 2),
            emprestimo_id=emprestimo.id,
            tipo_id=tipo_ocorrencia.id,
            tipo_descricao=tipo_ocorrencia.descricao,
        )
        entities.append(entity)

    models = [
        Ocorrencia.objects.get_or_create(**ocorrencia.to_dict())[0]
        for ocorrencia in entities
    ]

    yield models

    for model in reversed(models):
        model.delete()


@pytest.fixture
def lista_ocorrencias_canceladas(
    db, lista_emprestimos_em_andamento, lista_tipos_ocorrencia, test_user
):
    entities = []
    for i, (emprestimo, tipo_ocorrencia) in enumerate(
        zip(lista_emprestimos_em_andamento[:3], lista_tipos_ocorrencia[:3])
    ):
        entity = OcorrenciaEntity(
            id=i + 10,
            data_ocorrencia=date(2025, 10, 1),
            emprestimo_id=emprestimo.id,
            tipo_id=tipo_ocorrencia.id,
            tipo_descricao=tipo_ocorrencia.descricao,
            cancelado_em=date(2025, 10, 2),
            cancelado_por_id=test_user.id,
            motivo_cancelamento=f"Motivo cancelamento {i + 1}",
        )
        entities.append(entity)

    models = [
        Ocorrencia.objects.get_or_create(**ocorrencia.to_dict())[0]
        for ocorrencia in entities
    ]

    yield models

    for model in reversed(models):
        model.delete()


@pytest.fixture
def lista_ocorrencias_mescladas(
    db, lista_emprestimos_em_andamento, lista_tipos_ocorrencia, test_user
):
    """Mix of active and canceled occurrences"""
    entities = []

    for i in range(2):
        entity = OcorrenciaEntity(
            id=i + 20,
            data_ocorrencia=date(2025, 10, 1),
            emprestimo_id=lista_emprestimos_em_andamento[i].id,
            tipo_id=lista_tipos_ocorrencia[i].id,
            tipo_descricao=lista_tipos_ocorrencia[i].descricao,
        )
        entities.append(entity)

    for i in range(2, 4):
        entity = OcorrenciaEntity(
            id=i + 20,
            data_ocorrencia=date(2025, 10, 1),
            emprestimo_id=lista_emprestimos_em_andamento[i].id,
            tipo_id=lista_tipos_ocorrencia[i].id,
            tipo_descricao=lista_tipos_ocorrencia[i].descricao,
            cancelado_em=date(2025, 10, 2),
            cancelado_por_id=test_user.id,
            motivo_cancelamento=f"Cancelada {i}",
        )
        entities.append(entity)

    models = [
        Ocorrencia.objects.get_or_create(**ocorrencia.to_dict())[0]
        for ocorrencia in entities
    ]

    yield models

    for model in reversed(models):
        model.delete()


@pytest.mark.django_db
def test_listar_ocorrencias(admin_client, lista_ocorrencias):
    url = reverse_lazy("emprestimo:listar_ocorrencias")
    response = admin_client.get(url)

    for ocorrencia in lista_ocorrencias:
        assertContains(response, ocorrencia.tipo_descricao)
        assertContains(response, ocorrencia.emprestimo.id)
        assertContains(response, ocorrencia.emprestimo.aluno.nome)
        assertContains(response, ocorrencia.emprestimo.bem.descricao)

    assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")
    assert response.status_code == 200


@pytest.mark.django_db
def test_listar_ocorrencias_sem_permissao(client, test_user, lista_ocorrencias):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:listar_ocorrencias")
    response = client.get(url)

    assert response.status_code == 403
    assertTemplateNotUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")


@pytest.mark.django_db
def test_listar_ocorrencias_do_bem(admin_client, bem, lista_ocorrencias):
    ocorrencias_do_bem = [o for o in lista_ocorrencias if o.emprestimo.bem.id == bem.id]

    url = reverse_lazy("emprestimo:listar_ocorrencias_do_bem", args=[bem.id])
    response = admin_client.get(url)

    for ocorrencia in ocorrencias_do_bem:
        assertContains(response, ocorrencia.tipo_descricao)
        assertContains(response, ocorrencia.emprestimo.id)
        assertContains(response, ocorrencia.emprestimo.aluno.nome)

    outras_ocorrencias = [o for o in lista_ocorrencias if o.emprestimo.bem.id != bem.id]
    for ocorrencia in outras_ocorrencias:
        assertNotContains(response, ocorrencia.emprestimo.aluno.nome)

    assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")
    assert response.status_code == 200


@pytest.mark.django_db
def test_listar_ocorrencias_do_aluno(admin_client, aluno, lista_ocorrencias):
    ocorrencias_do_aluno = [
        o for o in lista_ocorrencias if o.emprestimo.aluno.id == aluno.id
    ]

    url = reverse_lazy("emprestimo:listar_ocorrencias_do_aluno", args=[aluno.id])
    response = admin_client.get(url)

    for ocorrencia in ocorrencias_do_aluno:
        assertContains(response, ocorrencia.tipo_descricao)
        assertContains(response, ocorrencia.emprestimo.id)
        assertContains(response, ocorrencia.emprestimo.bem.descricao)

    outras_ocorrencias = [
        o for o in lista_ocorrencias if o.emprestimo.aluno.id != aluno.id
    ]
    for ocorrencia in outras_ocorrencias:
        assertNotContains(response, ocorrencia.emprestimo.bem.descricao)

    assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")
    assert response.status_code == 200


@pytest.mark.django_db
def test_listar_ocorrencias_do_emprestimo(admin_client, emprestimo, lista_ocorrencias):
    ocorrencias_do_emprestimo = [
        o for o in lista_ocorrencias if o.emprestimo.id == emprestimo.id
    ]

    url = reverse_lazy(
        "emprestimo:listar_ocorrencias_do_emprestimo", args=[emprestimo.id]
    )
    response = admin_client.get(url)

    for ocorrencia in ocorrencias_do_emprestimo:
        assertContains(response, ocorrencia.tipo_descricao)
        assertContains(response, ocorrencia.emprestimo.id)
        assertContains(response, ocorrencia.data_ocorrencia.strftime("%d/%m/%Y"))

    outras_ocorrencias = [
        o for o in lista_ocorrencias if o.emprestimo.id != emprestimo.id
    ]
    for ocorrencia in outras_ocorrencias:
        assertNotContains(response, ocorrencia.tipo_descricao)

    assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")
    assert response.status_code == 200


@pytest.mark.django_db
def test_registrar_ocorrencia(admin_client, emprestimo, lista_tipos_ocorrencia):
    url = reverse_lazy("emprestimo:registrar_ocorrencia", args=[emprestimo.id])

    response = admin_client.get(url)
    assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_form.html")
    assert response.status_code == 200

    tipo_ocorrencia = lista_tipos_ocorrencia[0]
    data = {
        "data_ocorrencia": "2025-10-01",
        "tipo": tipo_ocorrencia.id,
        "emprestimo": emprestimo.id,
        "descricao": "Quebra do equipamento durante uso",
    }

    response = admin_client.post(url, data, follow=True)

    assert response.status_code == 200
    from emprestimo.models import Ocorrencia

    assert Ocorrencia.objects.filter(
        emprestimo=emprestimo, tipo=tipo_ocorrencia, data_ocorrencia="2025-10-01"
    ).exists()

    assertTemplateUsed(
        response, "emprestimo/emprestimo/emprestimo_detail.html"
    ) or assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")


@pytest.mark.django_db
def test_registrar_ocorrencia_sem_permissao(client, test_user, emprestimo):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:registrar_ocorrencia", args=[emprestimo.id])

    response = client.get(url)
    assert response.status_code == 403

    data = {
        "data_ocorrencia": "2025-10-01",
        "tipo": 1,
        "emprestimo": emprestimo.id,
        "descricao": "Tentativa sem permissão",
    }

    response = client.post(url, data)
    assert response.status_code == 403

    from emprestimo.models import Ocorrencia

    assert not Ocorrencia.objects.filter(
        emprestimo=emprestimo, data_ocorrencia="2025-10-01"
    ).exists()


@pytest.mark.django_db
def test_cancelar_ocorrencia(admin_client, ocorrencia):
    url = reverse_lazy("emprestimo:cancelar_ocorrencia", args=[ocorrencia.id])

    motivo = "Registro em duplicidade"
    response = admin_client.post(url, {"motivo_cancelamento": motivo}, follow=True)

    ocorrencia.refresh_from_db()
    assert response.status_code == 200
    assert ocorrencia.cancelado_em is not None
    assert ocorrencia.motivo_cancelamento == motivo
    assert ocorrencia.cancelado_por is not None

    assertContains(response, "Ocorrência cancelada com sucesso")
    assertTemplateUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")


@pytest.mark.django_db
def test_cancelar_ocorrencia_sem_permissao(client, test_user, ocorrencia):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:cancelar_ocorrencia", args=[ocorrencia.id])

    response = client.post(url, {"motivo_cancelamento": "Sem permissão"})

    ocorrencia.refresh_from_db()
    assert response.status_code == 403
    assert ocorrencia.cancelado_em is None
    assertTemplateNotUsed(response, "emprestimo/ocorrencia/ocorrencia_list.html")


@pytest.mark.django_db
def test_cancelar_ocorrencia_ja_cancelada(admin_client, ocorrencia_cancelada):
    url = reverse_lazy("emprestimo:cancelar_ocorrencia", args=[ocorrencia_cancelada.id])

    original_cancelamento = ocorrencia_cancelada.cancelado_em
    response = admin_client.post(
        url, {"motivo_cancelamento": "Novo motivo"}, follow=True
    )

    ocorrencia_cancelada.refresh_from_db()
    assert response.status_code == 400
    assert ocorrencia_cancelada.cancelado_em == original_cancelamento
    assertContains(response, "já cancelada")


@pytest.mark.django_db
def test_cancelar_ocorrencia_nao_encontrada(admin_client):
    url = reverse_lazy("emprestimo:cancelar_ocorrencia", args=[999])

    response = admin_client.post(
        url, {"motivo_cancelamento": "Motivo qualquer"}, follow=True
    )

    assert response.status_code == 404
