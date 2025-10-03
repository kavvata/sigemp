from datetime import date, datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateNotUsed,
    assertTemplateUsed,
)

from emprestimo.domain.entities import (
    OcorrenciaEntity,
    EmprestimoEntity,
    TipoOcorrenciaEntity,
)
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.models import Ocorrencia, Emprestimo, TipoOcorrencia

from ensino.domain.entities import (
    AlunoEntity,
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
)

from patrimonio.models import (
    Bem,
    EstadoConservacao,
    GrauFragilidade,
    MarcaModelo,
    TipoBem,
)

from patrimonio.domain.entities import BemEntity

from ensino.models import Aluno, Campus, Curso, FormaSelecao


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
    bens_models = [Bem.objects.get_or_create(**bem.to_dict())[0] for bem in bens_dict]

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
    model, _criado = Bem.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def campus(db):
    entity = CampusEntity(id=1, sigla="PNG", nome="Paranaguá")
    model, _criado = Campus.objects.get_or_create(
        **entity.to_dict(
            exclude=[
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
        **e.to_dict(exclude=["timestamps", "campus_sigla"])
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
    model, _criado = FormaSelecao.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


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
        Aluno.objects.get_or_create(**e.to_dict(exclude=["timestamps", "id"]))[0]
        for e in lista_entities
    ]

    yield lista_models

    for model in lista_models:
        model.delete()


@pytest.fixture
def lista_emprestimos_em_andamento(db, lista_alunos, bens):
    entities = []
    for i, (aluno, bem) in enumerate(zip(lista_alunos[:3], bens)):
        entity = EmprestimoEntity(
            id=i + 1,
            aluno_id=aluno.id,
            aluno_nome=aluno.nome,
            aluno_matricula=aluno.matricula,
            bem_id=bem.id,
            bem_descricao=bem.descricao,
            bem_patrimonio=bem.patrimonio,
            data_emprestimo=datetime.now().date() - timedelta(days=i),
            data_devolucao_prevista=datetime.now().date() + timedelta(days=7 - i),
            estado=EmprestimoEstadoEnum.ATIVO,
            observacoes=f"Empréstimo {i + 1} para atividades acadêmicas",
        )
        entities.append(entity)

    models = [Emprestimo.objects.get_or_create(**e.to_dict())[0] for e in entities]

    yield models

    for model in models:
        model.delete()


@pytest.fixture
def emprestimo(db, aluno, bem):
    entity = EmprestimoEntity(
        id=1,
        aluno_id=aluno.id,
        bem_id=bem.id,
        data_emprestimo=datetime.now().date(),
        data_devolucao_prevista=datetime.now().date() + timedelta(days=7),
        estado=EmprestimoEstadoEnum.ATIVO,
        bem_descricao=bem.descricao,
        bem_patrimonio=bem.patrimonio,
        aluno_nome=aluno.nome,
        aluno_matricula=aluno.matricula,
        observacoes="Empréstimo para aula de programação",
    )
    model, _criado = Emprestimo.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


@pytest.fixture
def emprestimo_devolvido(db, aluno, bem):
    entity = EmprestimoEntity(
        id=10,
        aluno_id=aluno.id,
        bem_id=bem.id,
        data_emprestimo=datetime.now().date() - timedelta(days=10),
        data_devolucao_prevista=datetime.now().date() - timedelta(days=3),
        data_devolucao=datetime.now().date() - timedelta(days=2),
        estado=EmprestimoEstadoEnum.FINALIZADO,
        observacoes="Empréstimo já devolvido",
    )
    model, _criado = Emprestimo.objects.get_or_create(**entity.to_dict())
    yield model

    model.delete()


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


@pytest.fixture
def ocorrencia(db, emprestimo, lista_tipos_ocorrencia, test_user):
    entity = OcorrenciaEntity(
        id=1,
        data_ocorrencia=date(2025, 10, 1),
        emprestimo_id=emprestimo.id,
        tipo_id=lista_tipos_ocorrencia[0].id,
        tipo_descricao=lista_tipos_ocorrencia[0].descricao,
    )
    model, _criado = Ocorrencia.objects.get_or_create(
        **entity.to_dict(
            exclude=[
                "tipo_descricao",
                "bem_descricao",
                "bem_patrimonio",
                "aluno_nome",
                "aluno_matricula",
                "timestamps",
            ]
        )
    )
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
    model, _criado = Ocorrencia.objects.get_or_create(
        **entity.to_dict(
            exclude=[
                "tipo_descricao",
                "bem_descricao",
                "bem_patrimonio",
                "aluno_nome",
                "aluno_matricula",
                "timestamps",
            ]
        )
    )
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
        Ocorrencia.objects.get_or_create(
            **ocorrencia.to_dict(
                exclude=[
                    "tipo_descricao",
                    "bem_descricao",
                    "bem_patrimonio",
                    "aluno_nome",
                    "aluno_matricula",
                    "timestamps",
                ]
            )
        )[0]
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
        Ocorrencia.objects.get_or_create(
            **ocorrencia.to_dict(
                exclude=[
                    "tipo_descricao",
                    "bem_descricao",
                    "bem_patrimonio",
                    "aluno_nome",
                    "aluno_matricula",
                    "timestamps",
                ]
            )
        )[0]
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
        Ocorrencia.objects.get_or_create(
            **ocorrencia.to_dict(
                exclude=[
                    "tipo_descricao",
                    "bem_descricao",
                    "bem_patrimonio",
                    "aluno_nome",
                    "aluno_matricula",
                    "timestamps",
                ]
            )
        )[0]
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
        assertContains(response, ocorrencia.tipo.descricao)
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
        assertContains(response, ocorrencia.tipo.descricao)
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
        assertContains(response, ocorrencia.tipo.descricao)
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
        assertContains(response, ocorrencia.tipo.descricao)
        assertContains(response, ocorrencia.emprestimo.id)
        assertContains(response, ocorrencia.data_ocorrencia.strftime("%d/%m/%Y"))

    outras_ocorrencias = [
        o for o in lista_ocorrencias if o.emprestimo.id != emprestimo.id
    ]
    for ocorrencia in outras_ocorrencias:
        assertNotContains(response, ocorrencia.tipo.descricao)

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
