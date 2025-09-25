from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.usecases import (
    ListarEmprestimosUsecase,
    CadastrarEmprestimoUsecase,
    EditarEmprestimoUsecase,
    RemoverEmprestimoUsecase,
)


@pytest.fixture
def emprestimo():
    return EmprestimoEntity(
        id=1,
        data_emprestimo="2025-09-01",
        data_devolucao_prevista="2025-09-15",
        data_devolucao=None,
        estado=1,
        bem_id=1,
        aluno_id=1,
    )


@pytest.fixture
def lista_emprestimos_em_andamento():
    return [
        EmprestimoEntity(
            id=i,
            data_emprestimo="2025-09-01",
            data_devolucao_prevista="2025-09-15",
            data_devolucao=None,
            estado=1,
            bem_id=i,
            aluno_id=1,
        )
        for i in range(1, 5)
    ]


def test_listar_emprestimos(lista_emprestimos_em_andamento):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_emprestimos.return_value = lista_emprestimos_em_andamento
    policy.pode_listar.return_value = True

    usecase = ListarEmprestimosUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_emprestimos.assert_called()
    policy.pode_listar.assert_called()

    assert isinstance(result, ResultSuccess)
    assert result.value == lista_emprestimos_em_andamento


def test_nao_pode_listar_emprestimos_usecase(lista_emprestimos_em_andamento):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_listar.return_value = False
    usecase = ListarEmprestimosUsecase(repo, policy)
    result = usecase.execute()

    policy.pode_listar.assert_called()
    assert isinstance(result, ResultError)


def test_cadastrar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    repo.buscar_bem.return_value = mock.Mock(estado="Disponível")
    repo.buscar_emprestimos_ativos_por_aluno.return_value = []
    repo.cadastrar_emprestimo.return_value = emprestimo
    policy.pode_criar.return_value = True

    usecase = CadastrarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    repo.buscar_bem.assert_called_with(emprestimo.bem_id)
    repo.buscar_emprestimos_ativos_por_aluno.assert_called_with(emprestimo.aluno_id)
    repo.cadastrar_emprestimo.assert_called_with(emprestimo, user)

    assert isinstance(result, ResultSuccess)
    assert result.value == emprestimo


def test_nao_pode_cadastrar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_criar.return_value = True

    repo.buscar_bem.return_value = mock.Mock(estado="Emprestado")
    repo.buscar_emprestimos_ativos_por_aluno.return_value = []
    usecase = CadastrarEmprestimoUsecase(repo, policy)

    result = usecase.execute(emprestimo)

    repo.buscar_bem.assert_called_with(emprestimo.bem_id)
    assert isinstance(result, ResultError)


def test_nao_pode_cadastrar_emprestimo_quando_aluno_tem_ativo(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_criar.return_value = True

    repo.buscar_bem.return_value = mock.Mock(estado="Disponível")
    repo.buscar_emprestimos_ativos_por_aluno.return_value = [mock.Mock()]
    usecase = CadastrarEmprestimoUsecase(repo, policy)

    result = usecase.execute(emprestimo)

    repo.buscar_emprestimos_ativos_por_aluno.assert_called_with(emprestimo.aluno_id)
    assert isinstance(result, ResultError)


def test_editar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    policy.pode_editar.return_value = True
    repo.buscar_por_id.return_value = emprestimo
    repo.editar_emprestimo.return_value = emprestimo

    usecase = EditarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    repo.buscar_por_id.assert_called_with(emprestimo.id)
    repo.editar_emprestimo.assert_called_with(emprestimo, user)

    assert isinstance(result, ResultSuccess)
    assert result.value == emprestimo


def test_nao_pode_editar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = False

    usecase = EditarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    policy.pode_editar.assert_called()
    assert isinstance(result, ResultError)


def test_remover_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    policy.pode_remover.return_value = True
    repo.buscar_por_id.return_value = emprestimo

    usecase = RemoverEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo.id)

    repo.buscar_por_id.assert_called_with(emprestimo.id)
    repo.remover_emprestimo.assert_called_with(emprestimo, user)

    assert isinstance(result, ResultSuccess)


def test_nao_pode_remover_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_remover.return_value = False

    usecase = RemoverEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo.id)

    policy.pode_remover.assert_called()
    assert isinstance(result, ResultError)
