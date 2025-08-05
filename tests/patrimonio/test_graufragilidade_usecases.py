from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from patrimonio.usecases import (
    ListarGrauFragilidadeUsecase,
    CadastrarGrauFragilidadeUsecase,
    EditarGrauFragilidadeUsecase,
    RemoverGrauFragilidadeUsecase,
)

from patrimonio.domain.entities import GrauFragilidadeEntity


@pytest.fixture
def grau_fragilidade():
    return GrauFragilidadeEntity(id=3, descricao="Médio", nivel=3)


@pytest.fixture
def lista_grau_fragilidade():
    return [
        GrauFragilidadeEntity(id=1, descricao="Péssimo", nivel=1),
        GrauFragilidadeEntity(id=2, descricao="Mau", nivel=2),
        GrauFragilidadeEntity(id=3, descricao="Médio", nivel=3),
        GrauFragilidadeEntity(id=4, descricao="Bom", nivel=4),
        GrauFragilidadeEntity(id=5, descricao="Excelente", nivel=5),
    ]


def test_listar_grau_fragilidade(lista_grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_grau_fragilidade.return_value = lista_grau_fragilidade
    policy.pode_listar.return_value = True

    usecase = ListarGrauFragilidadeUsecase(repo, policy)

    if usecase.pode_listar():
        result = usecase.execute()

    repo.listar_grau_fragilidade.assert_called_with()
    policy.pode_listar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_grau_fragilidade


def test_nao_pode_listar_grau_fragilidade_usecase(lista_grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_grau_fragilidade.return_value = lista_grau_fragilidade
    policy.pode_listar.return_value = False

    usecase = ListarGrauFragilidadeUsecase(repo, policy)

    result = usecase.execute()

    repo.listar_grau_fragilidade.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_grau_fragilidade_usecase(grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_grau_fragilidade.return_value = grau_fragilidade
    policy.pode_criar.return_value = True
    policy.user = user

    usecase = CadastrarGrauFragilidadeUsecase(repo, policy)

    if usecase.pode_criar():
        result = usecase.execute(grau_fragilidade.descricao, grau_fragilidade.nivel)

    repo.cadastrar_grau_fragilidade.assert_called_with(
        grau_fragilidade.descricao, grau_fragilidade.nivel, user
    )
    policy.pode_criar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == grau_fragilidade


def test_nao_pode_cadastrar_grau_fragilidade_usecase(grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_grau_fragilidade.return_value = grau_fragilidade
    policy.pode_criar.return_value = False
    policy.user = user

    usecase = CadastrarGrauFragilidadeUsecase(repo, policy)

    result = usecase.execute(grau_fragilidade.descricao, grau_fragilidade.nivel)

    repo.cadastrar_grau_fragilidade.assert_not_called()
    policy.pode_criar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_editar_grau_fragilidade_usecase(grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = grau_fragilidade
    repo.editar_grau_fragilidade.return_value = grau_fragilidade
    policy.pode_editar.return_value = True
    policy.user = user

    usecase = EditarGrauFragilidadeUsecase(repo, policy)

    result = usecase.get_grau_fragilidade(grau_fragilidade.id)
    encontrado = result.value

    assert encontrado

    result = usecase.execute(encontrado.id, encontrado.descricao, encontrado.nivel)

    repo.buscar_por_id.assert_called_with(grau_fragilidade.id)
    repo.editar_grau_fragilidade.assert_called_with(
        grau_fragilidade.id,
        grau_fragilidade.descricao,
        grau_fragilidade.nivel,
        user,
    )
    policy.pode_editar.assert_called_with(grau_fragilidade)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == grau_fragilidade


def test_nao_pode_editar_grau_fragilidade_usecase(grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = grau_fragilidade
    repo.editar_grau_fragilidade.return_value = grau_fragilidade
    policy.pode_editar.return_value = False
    policy.user = user

    usecase = EditarGrauFragilidadeUsecase(repo, policy)

    result = usecase.get_grau_fragilidade(grau_fragilidade.id)
    assert not result
    assert isinstance(result, ResultError)

    result = usecase.execute(
        grau_fragilidade.id,
        grau_fragilidade.descricao,
        grau_fragilidade.nivel,
    )

    repo.buscar_por_id.assert_called_with(grau_fragilidade.id)
    repo.editar_grau_fragilidade.assert_not_called()
    policy.pode_editar.assert_called_with(grau_fragilidade)

    assert not result
    assert isinstance(result, ResultError)


def test_remover_grau_fragilidade_usecase(grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = grau_fragilidade
    repo.remover_grau_fragilidade.return_value = grau_fragilidade
    policy.pode_remover.return_value = True
    policy.user = user

    usecase = RemoverGrauFragilidadeUsecase(repo, policy)

    result = usecase.execute(grau_fragilidade.id)

    repo.remover_grau_fragilidade.assert_called_with(grau_fragilidade.id, user)
    policy.pode_remover.assert_called_with(grau_fragilidade)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == grau_fragilidade


def test_nao_pode_remover_grau_fragilidade_usecase(grau_fragilidade):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = grau_fragilidade
    repo.remover_grau_fragilidade.return_value = grau_fragilidade
    policy.pode_remover.return_value = False
    policy.user = user

    usecase = RemoverGrauFragilidadeUsecase(repo, policy)

    result = usecase.execute(grau_fragilidade.id)

    repo.remover_grau_fragilidade.assert_not_called()
    policy.pode_remover.assert_called_with(grau_fragilidade)

    assert not result
    assert isinstance(result, ResultError)
