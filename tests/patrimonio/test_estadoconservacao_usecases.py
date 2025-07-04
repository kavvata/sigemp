from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from patrimonio.usecases import (
    ListarEstadosConservacaoUsecase,
    CadastrarEstadoConservacaoUsecase,
    EditarEstadoConservacaoUsecase,
    RemoverEstadoConservacaoUsecase,
)


@pytest.fixture
def estado_conservacao():
    return {"id": 3, "descricao": "Médio", "nivel": 3}


@pytest.fixture
def lista_estados_conservacao():
    return [
        {"id": 1, "descricao": "Péssimo", "nivel": 1},
        {"id": 2, "descricao": "Mau", "nivel": 2},
        {"id": 3, "descricao": "Médio", "nivel": 3},
        {"id": 4, "descricao": "Bom", "nivel": 4},
        {"id": 5, "descricao": "Excelente", "nivel": 5},
    ]


def test_listar_estados_conservacao(lista_estados_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_estados_conservacao.return_value = lista_estados_conservacao
    policy.pode_listar.return_value = True

    usecase = ListarEstadosConservacaoUsecase(repo, policy)

    if usecase.pode_listar():
        result = usecase.execute()

    repo.listar_estados_conservacao.assert_called_with()
    policy.pode_listar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_estados_conservacao


def test_nao_pode_listar_estados_conservacao_usecase(lista_estados_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_estados_conservacao.return_value = lista_estados_conservacao
    policy.pode_listar.return_value = False

    usecase = ListarEstadosConservacaoUsecase(repo, policy)

    result = usecase.execute()

    repo.listar_estados_conservacao.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_estado_conservacao_usecase(estado_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_estado_conservacao.return_value = estado_conservacao
    policy.pode_criar.return_value = True
    policy.user = user

    usecase = CadastrarEstadoConservacaoUsecase(repo, policy)

    if usecase.pode_criar():
        result = usecase.execute(
            estado_conservacao["descricao"], estado_conservacao["nivel"]
        )

    repo.cadastrar_estado_conservacao.assert_called_with(
        estado_conservacao["descricao"], estado_conservacao["nivel"], user
    )
    policy.pode_criar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == estado_conservacao


def test_nao_pode_cadastrar_estado_conservacao_usecase(estado_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_estado_conservacao.return_value = estado_conservacao
    policy.pode_criar.return_value = False
    policy.user = user

    usecase = CadastrarEstadoConservacaoUsecase(repo, policy)

    result = usecase.execute(
        estado_conservacao["descricao"], estado_conservacao["nivel"]
    )

    repo.cadastrar_estado_conservacao.assert_not_called()
    policy.pode_criar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_editar_estado_conservacao_usecase(estado_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = estado_conservacao
    repo.editar_estado_conservacao.return_value = estado_conservacao
    policy.pode_editar.return_value = True
    policy.user = user

    usecase = EditarEstadoConservacaoUsecase(repo, policy)

    result = usecase.get_estado_conservacao(estado_conservacao["id"])
    encontrado = result.value

    assert encontrado

    result = usecase.execute(
        encontrado["id"], encontrado["descricao"], encontrado["nivel"]
    )

    repo.buscar_por_id.assert_called_with(estado_conservacao["id"])
    repo.editar_estado_conservacao.assert_called_with(
        estado_conservacao["id"],
        estado_conservacao["descricao"],
        estado_conservacao["nivel"],
        user,
    )
    policy.pode_editar.assert_called_with(estado_conservacao)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == estado_conservacao


def test_nao_pode_editar_estado_conservacao_usecase(estado_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = estado_conservacao
    repo.editar_estado_conservacao.return_value = estado_conservacao
    policy.pode_editar.return_value = False
    policy.user = user

    usecase = EditarEstadoConservacaoUsecase(repo, policy)

    result = usecase.get_estado_conservacao(estado_conservacao["id"])
    assert not result
    assert isinstance(result, ResultError)

    result = usecase.execute(
        estado_conservacao["id"],
        estado_conservacao["descricao"],
        estado_conservacao["nivel"],
    )

    repo.buscar_por_id.assert_called_with(estado_conservacao["id"])
    repo.editar_estado_conservacao.assert_not_called()
    policy.pode_editar.assert_called_with(estado_conservacao)

    assert not result
    assert isinstance(result, ResultError)


def test_remover_estado_conservacao_usecase(estado_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = estado_conservacao
    repo.remover_estado_conservacao.return_value = estado_conservacao
    policy.pode_remover.return_value = True
    policy.user = user

    usecase = RemoverEstadoConservacaoUsecase(repo, policy)

    result = usecase.execute(estado_conservacao["id"])

    repo.remover_estado_conservacao.assert_called_with(estado_conservacao["id"], user)
    policy.pode_remover.assert_called_with(estado_conservacao)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == estado_conservacao


def test_nao_pode_remover_estado_conservacao_usecase(estado_conservacao):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = estado_conservacao
    repo.remover_estado_conservacao.return_value = estado_conservacao
    policy.pode_remover.return_value = False
    policy.user = user

    usecase = RemoverEstadoConservacaoUsecase(repo, policy)

    result = usecase.execute(estado_conservacao["id"])

    repo.remover_estado_conservacao.assert_not_called()
    policy.pode_remover.assert_called_with(estado_conservacao)

    assert not result
    assert isinstance(result, ResultError)
