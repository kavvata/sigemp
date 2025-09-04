from unittest import mock

import pytest

from core.types import ResultError, ResultSuccess
from ensino.domain.entities import AlunoEntity
from ensino.usecases import (
    CadastrarAlunoUsecase,
    EditarAlunoUsecase,
    ListarAlunosUsecase,
    RemoverAlunoUsecase,
)


@pytest.fixture
def aluno():
    return AlunoEntity(
        id=1,
        nome="João da Silva",
        cpf="12345678901",
        email="joao.silva@ifpr.edu.br",
        matricula="2025001",
        telefone="41999990001",
        forma_selecao_id=1,
        curso_id=1,
    )


@pytest.fixture
def lista_alunos():
    return [
        AlunoEntity(
            id=1,
            nome="João da Silva",
            cpf="12345678901",
            email="joao.silva@ifpr.edu.br",
            matricula="2025001",
            telefone="41999990001",
            forma_selecao_id=1,
            curso_id=1,
        ),
        AlunoEntity(
            id=2,
            nome="Ana Pereira",
            nome_responsavel="Carlos Pereira",
            cpf="98765432100",
            email="ana.pereira@ifpr.edu.br",
            matricula="2025002",
            telefone="41999990002",
            forma_selecao_id=1,
            curso_id=1,
        ),
        AlunoEntity(
            id=3,
            nome="Lucas Andrade",
            nome_responsavel="Fernanda Andrade",
            cpf="45678912300",
            email="lucas.andrade@ifpr.edu.br",
            matricula="2025003",
            telefone="41999990003",
            forma_selecao_id=2,
            curso_id=2,
        ),
        AlunoEntity(
            id=4,
            nome="Beatriz Costa",
            cpf="32165498700",
            email="beatriz.costa@ifpr.edu.br",
            matricula="2025004",
            telefone="41999990004",
            forma_selecao_id=2,
            curso_id=2,
        ),
        AlunoEntity(
            id=5,
            nome="Marcos Oliveira",
            cpf="15975348620",
            email="marcos.oliveira@ifpr.edu.br",
            matricula="2025005",
            telefone="41999990005",
            forma_selecao_id=3,
            curso_id=3,
        ),
    ]


def test_listar_alunos(lista_alunos: list[AlunoEntity]):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_alunos.return_value = lista_alunos
    policy.pode_listar.return_value = True

    usecase = ListarAlunosUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_alunos.assert_called()
    policy.pode_listar.assert_called()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_alunos


def test_nao_pode_listar_alunos(lista_alunos: list[AlunoEntity]):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_alunos.return_value = lista_alunos
    policy.pode_listar.return_value = False

    usecase = ListarAlunosUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_alunos.assert_not_called()
    policy.pode_listar.assert_called()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_aluno(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_criar.return_value = True
    repo.buscar.return_value = None
    repo.cadastrar_aluno.return_value = aluno

    usecase = CadastrarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(matricula=aluno.matricula)
    repo.buscar.assert_any_call(cpf=aluno.cpf)
    repo.buscar.assert_any_call(email=aluno.email)
    repo.cadastrar_aluno.assert_called_with(aluno, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == aluno


def test_nao_pode_cadastrar_aluno(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_criar.return_value = False

    usecase = CadastrarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.cadastrar_aluno.assert_not_called()
    repo.buscar.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_cadastrar_aluno_matricula_repetida(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_criar.return_value = True
    repo.buscar.side_effect = lambda **f: aluno if "matricula" in f else None

    usecase = CadastrarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(matricula=aluno.matricula)
    repo.cadastrar_aluno.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_cadastrar_aluno_cpf_repetido(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_criar.return_value = True
    repo.buscar.side_effect = lambda **f: aluno if "cpf" in f else None

    usecase = CadastrarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(cpf=aluno.cpf)
    repo.cadastrar_aluno.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_cadastrar_aluno_email_repetido(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_criar.return_value = True
    repo.buscar.side_effect = lambda **f: aluno if "email" in f else None

    usecase = CadastrarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(email=aluno.email)
    repo.cadastrar_aluno.assert_not_called()
    assert isinstance(result, ResultError)


def test_editar_aluno(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = True
    repo.buscar.return_value = None
    repo.editar_aluno.return_value = aluno

    usecase = EditarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(matricula=aluno.matricula)
    repo.buscar.assert_any_call(cpf=aluno.cpf)
    repo.buscar.assert_any_call(email=aluno.email)
    repo.editar_aluno.assert_called_with(aluno, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == aluno


def test_nao_pode_editar_aluno(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = False

    usecase = EditarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.editar_aluno.assert_not_called()
    repo.buscar.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_editar_aluno_matricula_repetida(
    aluno: AlunoEntity, lista_alunos: list[AlunoEntity]
):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = True
    repo.buscar.side_effect = lambda **f: lista_alunos[1] if "matricula" in f else None

    usecase = EditarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(matricula=aluno.matricula)
    repo.editar_aluno.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_editar_aluno_cpf_repetido(
    aluno: AlunoEntity, lista_alunos: list[AlunoEntity]
):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = True
    repo.buscar.side_effect = lambda **f: lista_alunos[1] if "cpf" in f else None

    usecase = EditarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(cpf=aluno.cpf)
    repo.editar_aluno.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_editar_aluno_email_repetido(
    aluno: AlunoEntity, lista_alunos: list[AlunoEntity]
):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = True
    repo.buscar.side_effect = lambda **f: lista_alunos[1] if "email" in f else None

    usecase = EditarAlunoUsecase(repo, policy)
    result = usecase.execute(aluno)

    repo.buscar.assert_any_call(email=aluno.email)
    repo.editar_aluno.assert_not_called()
    assert isinstance(result, ResultError)


def test_remover_aluno(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_remover.return_value = True
    repo.buscar_por_id.return_value = aluno
    repo.remover_aluno.return_value = aluno

    usecase = RemoverAlunoUsecase(repo, policy)
    result = usecase.execute(aluno.id)

    repo.remover_aluno.assert_called_with(aluno.id, user)
    assert isinstance(result, ResultSuccess)
    assert result.value == aluno


def test_nao_pode_remover_aluno(aluno: AlunoEntity):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_remover.return_value = False
    repo.buscar_por_id.return_value = aluno
    repo.remover_aluno.return_value = None

    usecase = RemoverAlunoUsecase(repo, policy)
    result = usecase.execute(aluno.id)

    repo.remover_aluno.assert_not_called()
    assert isinstance(result, ResultError)
