from unittest import mock
import pytest

from core.types import ResultSuccess
from patrimonio.usecases import (
    ListarTiposBemUsecase,
    CadastrarTipoBemUsecase,
    EditarTipoBemUsecase,
    RemoverTipoBemUsecase,
)


@pytest.fixture
def tipo_bem():
    return {"id": 1, "descricao": "Projetor", "ativo": True}


@pytest.fixture
def lista_tipos_bem():
    return [
        {"id": 1, "descricao": "Projetor", "ativo": True},
        {"id": 2, "descricao": "Notebook Dell", "ativo": True},
        {"id": 3, "descricao": "Frasco laboratorio", "ativo": True},
    ]


def listar_tipos_bem(lista_tipos_bem):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_tipos_bem.return_value = lista_tipos_bem
    policy.pode_listar.return_value = True

    usecase = ListarTiposBemUsecase(repo, policy)

    if usecase.pode_listar():
        result = usecase.execute()

    repo.listar_tipos_bem.assert_called_with()
    policy.pode_listar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_tipos_bem


def test_cadastrar_tipo_bem_usecase(tipo_bem):
    repo = mock.Mock()
    policy = mock.Mock()
    repo.cadastrar_tipo_bem.return_value = tipo_bem
    policy.pode_criar.return_value = True

    usecase = CadastrarTipoBemUsecase(repo, policy)

    if usecase.pode_criar():
        result = usecase.execute(tipo_bem["descricao"])

    repo.cadastrar_tipo_bem.assert_called_with(tipo_bem["descricao"])
    policy.pode_criar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_bem


def test_editar_tipo_bem_usecase(tipo_bem):
    repo = mock.Mock()
    policy = mock.Mock()
    repo.buscar_por_id.return_value = tipo_bem
    repo.editar_tipo_bem.return_value = tipo_bem
    policy.pode_editar.return_value = True

    usecase = EditarTipoBemUsecase(repo, policy)

    result = usecase.get_tipo_bem(tipo_bem["id"])
    encontrado = result.value

    assert encontrado

    result = usecase.execute(encontrado["id"], encontrado["descricao"])

    repo.buscar_por_id.assert_called_with(tipo_bem["id"])
    repo.editar_tipo_bem.assert_called_with(tipo_bem["id"], tipo_bem["descricao"])
    policy.pode_editar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_bem


def test_remover_tipo_bem_usecase(tipo_bem):
    repo = mock.Mock()
    policy = mock.Mock()
    repo.remover_tipo_bem.return_value = tipo_bem
    policy.pode_remover.return_value = True

    usecase = RemoverTipoBemUsecase(repo, policy)

    result = usecase.execute(tipo_bem["id"])

    repo.remover_tipo_bem.assert_called_with(tipo_bem["id"])
    policy.pode_remover.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_bem
