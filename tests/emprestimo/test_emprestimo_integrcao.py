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

from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.infrastructure.mappers import EmprestimoMapper
from ensino.domain.entities import (
    AlunoEntity,
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
)
from ensino.models import Aluno, Campus, Curso, FormaSelecao
from patrimonio.domain.entities import BemEntity
from patrimonio.models import (
    Bem,
    EstadoConservacao,
    GrauFragilidade,
    MarcaModelo,
    TipoBem,
)
from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.models import Emprestimo


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


@pytest.mark.django_db
def test_listar_emprestimos(lista_emprestimos_em_andamento, admin_client):
    url = reverse_lazy("emprestimo:listar_emprestimos")
    response = admin_client.get(url)

    for emprestimo in lista_emprestimos_em_andamento:
        assertContains(response, emprestimo.id)
        assertContains(response, emprestimo.aluno.nome)
        assertContains(response, emprestimo.bem.descricao)

    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_list.html")
    assert response.status_code == 200


@pytest.mark.django_db
def test_nao_pode_listar_emprestimos(client, test_user, lista_emprestimos_em_andamento):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:listar_emprestimos")
    response = client.get(url)

    assert response.status_code == 403
    assertTemplateNotUsed(response, "emprestimo/emprestimo/emprestimo_list.html")


@pytest.mark.django_db
def test_cadastrar_emprestimo(admin_client, aluno, bem):
    url = reverse_lazy("emprestimo:criar_emprestimo")

    response = admin_client.get(url)
    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_form.html")
    assert response.status_code == 200

    data = {
        "aluno": aluno.id,
        "bem": bem.id,
        "data_emprestimo": datetime.now().date(),
        "data_devolucao_prevista": datetime.now().date() + timedelta(days=7),
        "observacoes": "Novo empréstimo para aula prática",
    }

    response = admin_client.post(url, data, follow=True)

    emprestimo_cadastrado = Emprestimo.objects.filter(aluno=aluno, bem=bem)
    assert response.status_code == 200
    assert emprestimo_cadastrado.exists()
    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_list.html")


@pytest.mark.django_db
def test_nao_pode_cadastrar_emprestimo(client, test_user, aluno, bem):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:criar_emprestimo")

    response = client.get(url)
    assert response.status_code == 403

    data = {
        "aluno": aluno.id,
        "bem": bem.id,
        "data_emprestimo": datetime.now().date(),
        "data_devolucao_prevista": datetime.now().date() + timedelta(days=7),
        "observacoes": "Tentativa de empréstimo sem permissão",
    }

    response = client.post(url, data)
    assert response.status_code == 403
    assert not Emprestimo.objects.filter(aluno=aluno, bem=bem).exists()


@pytest.mark.django_db
def test_nao_pode_cadastrar_emprestimo_quando_aluno_tem_ativo(
    admin_client, aluno, bem, emprestimo
):
    url = reverse_lazy("emprestimo:criar_emprestimo")

    data = {
        "aluno": aluno.id,
        "bem": bem.id,  # Mesmo bem ou bem diferente
        "data_emprestimo": datetime.now().date(),
        "data_devolucao_prevista": datetime.now().date() + timedelta(days=7),
        "observacoes": "Tentativa de empréstimo com aluno que já tem ativo",
    }

    response = admin_client.post(url, data)

    assert response.status_code == 302
    assert (
        Emprestimo.objects.filter(aluno=aluno, data_devolucao__isnull=True).count() == 1
    )


def test_visualizar_detalhes_emprestimo_ativo(admin_client, emprestimo: Emprestimo):
    url = reverse_lazy("emprestimo:visualizar_emprestimo", args=[emprestimo.id])

    response = admin_client.get(url)

    assertContains(response, emprestimo.data_emprestimo.strftime("%d/%m/%Y"))
    assertContains(response, emprestimo.observacoes)
    assertContains(response, emprestimo.data_devolucao_prevista.strftime("%d/%m/%Y"))
    assertContains(response, emprestimo.aluno.nome)
    assertContains(response, emprestimo.aluno.matricula)
    assertContains(response, emprestimo.bem.descricao)
    assertContains(response, emprestimo.bem.patrimonio)
    assertContains(response, emprestimo.estado)

    assertContains(response, "Gerar termo de responsabilidade")
    assertNotContains(response, "Gerar termo de devolução")

    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_detail.html")
    assert response.status_code == 200


def test_visualizar_detalhes_emprestimo_devolvido(
    admin_client, emprestimo_devolvido: Emprestimo
):
    url = reverse_lazy(
        "emprestimo:visualizar_emprestimo", args=[emprestimo_devolvido.id]
    )

    response = admin_client.get(url)

    assertContains(response, emprestimo_devolvido.data_emprestimo.strftime("%d/%m/%Y"))
    assertContains(response, emprestimo_devolvido.observacoes)
    assertContains(
        response, emprestimo_devolvido.data_devolucao_prevista.strftime("%d/%m/%Y")
    )
    assertContains(response, emprestimo_devolvido.data_devolucao.strftime("%d/%m/%Y"))
    assertContains(response, emprestimo_devolvido.aluno.nome)
    assertContains(response, emprestimo_devolvido.aluno.matricula)
    assertContains(response, emprestimo_devolvido.bem.descricao)
    assertContains(response, emprestimo_devolvido.bem.patrimonio)
    assertContains(response, emprestimo_devolvido.estado)

    assertNotContains(response, "Gerar termo de responsabilidade")
    assertContains(response, "Gerar termo de devolução")

    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_detail.html")
    assert response.status_code == 200


@pytest.mark.django_db
def test_registrar_devolucao_emprestimo(admin_client, emprestimo):
    url = reverse_lazy("emprestimo:registrar_devolucao", args=[emprestimo.id])

    response = admin_client.post(url, follow=True)

    emprestimo.refresh_from_db()
    assert response.status_code == 200
    assert emprestimo.data_devolucao is not None
    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_detail.html")


@pytest.mark.django_db
def test_nao_pode_registrar_devolucao_emprestimo_ja_devolvido(
    admin_client, emprestimo_devolvido: Emprestimo
):
    url = reverse_lazy("emprestimo:registrar_devolucao", args=[emprestimo_devolvido.id])

    data_original = emprestimo_devolvido.data_devolucao

    response = admin_client.post(url, follow=True)

    emprestimo_devolvido.refresh_from_db()
    assert data_original == emprestimo_devolvido.data_devolucao
    assertContains(response, "já devolvido")


@pytest.mark.django_db
def test_editar_emprestimo(admin_client, emprestimo, lista_alunos):
    url = reverse_lazy("emprestimo:editar_emprestimo", args=[emprestimo.id])

    response = admin_client.get(url)
    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_form.html")
    assert response.status_code == 200

    existente = emprestimo

    novo_aluno = lista_alunos[1]
    data = EmprestimoMapper.from_model(existente).to_dict()
    del data["data_devolucao"]
    del data["devolucao_ciente_por_id"]
    data["aluno"] = novo_aluno.id
    data["bem"] = data.pop("bem_id")

    response = admin_client.post(url, data, follow=True)

    existente.refresh_from_db()
    assert response.status_code == 200
    assert existente.aluno.id == novo_aluno.id
    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_list.html")


@pytest.mark.django_db
def test_nao_pode_editar_emprestimo(client, test_user, emprestimo):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:editar_emprestimo", args=[emprestimo.id])

    response = client.get(url)
    assert response.status_code == 403

    data = EmprestimoMapper.from_model(emprestimo).to_dict()
    del data["data_devolucao"]
    del data["devolucao_ciente_por_id"]
    data["bem"] = data.pop("bem_id")
    data["aluno"] = data.pop("aluno_id")

    response = client.post(url, data)
    print(response.text)
    assert response.status_code == 403


@pytest.mark.django_db
def test_remover_emprestimo(admin_client, emprestimo):
    url = reverse_lazy("emprestimo:remover_emprestimo", args=[emprestimo.id])

    response = admin_client.get(url, follow=True)

    assert response.status_code == 200
    assert not Emprestimo.objects.filter(
        id=emprestimo.id, removido_em__isnull=True
    ).exists()
    assertTemplateUsed(response, "emprestimo/emprestimo/emprestimo_list.html")


@pytest.mark.django_db
def test_nao_pode_remover_emprestimo(client, test_user, emprestimo):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:remover_emprestimo", args=[emprestimo.id])

    response = client.post(url, follow=True)

    assert response.status_code == 403
    assert Emprestimo.objects.filter(id=emprestimo.id).exists()


@pytest.mark.django_db
def test_gerar_termo_responsabilidade_sucesso(admin_client, emprestimo):
    url = reverse_lazy("emprestimo:gerar_termo_responsabilidade", args=[emprestimo.id])

    response = admin_client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"


@pytest.mark.django_db
def test_gerar_termo_responsabilidade_sem_permissao(client, test_user, emprestimo):
    client.force_login(test_user)
    url = reverse_lazy("emprestimo:gerar_termo_responsabilidade", args=[emprestimo.id])

    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_nao_pode_gerar_termo_responsabilidade_emprestimo_finalizado(
    admin_client, emprestimo_devolvido
):
    url = reverse_lazy(
        "emprestimo:gerar_termo_responsabilidade", args=[emprestimo_devolvido.id]
    )

    response = admin_client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_gerar_termo_responsabilidade_erro_repo(admin_client, emprestimo):
    emprestimo_id = emprestimo.id
    emprestimo.soft_delete()

    url = reverse_lazy("emprestimo:gerar_termo_responsabilidade", args=[emprestimo_id])

    response = admin_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_gerar_termo_devolucao_sucesso(admin_client, emprestimo_devolvido):
    url = reverse_lazy(
        "emprestimo:gerar_termo_devolucao", args=[emprestimo_devolvido.id]
    )

    response = admin_client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"


@pytest.mark.django_db
def test_gerar_termo_devolucao_sem_permissao(client, test_user, emprestimo_devolvido):
    client.force_login(test_user)
    url = reverse_lazy(
        "emprestimo:gerar_termo_devolucao", args=[emprestimo_devolvido.id]
    )

    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_gerar_termo_devolucao_erro_repo(admin_client, emprestimo_devolvido):
    emprestimo_id = emprestimo_devolvido.id
    emprestimo_devolvido.soft_delete()

    url = reverse_lazy("emprestimo:gerar_termo_devolucao", args=[emprestimo_id])

    response = admin_client.get(url)

    assert response.status_code == 404
