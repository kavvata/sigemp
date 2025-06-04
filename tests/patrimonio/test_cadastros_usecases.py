from unittest import mock
import pytest

from core.types import ResultSuccess
from patrimonio.usecases import (
    listar_tipos_bem_usecase,
    cadastrar_tipo_bem_usecase,
    editar_tipo_bem_usecase,
    remover_tipo_bem_usecase,
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
    repo.listar_tipos_bem.return_value = lista_tipos_bem

    result = listar_tipos_bem_usecase(repo)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_tipos_bem


def test_cadastrar_tipo_bem_usecase(tipo_bem):
    repo = mock.Mock()
    repo.cadastrar_tipo_bem.return_value = tipo_bem
    result = cadastrar_tipo_bem_usecase(tipo_bem["descricao"], repo)

    repo.cadastrar_tipo_bem.assert_called_with(tipo_bem["descricao"])

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_bem


def test_editar_tipo_bem_usecase(tipo_bem):
    repo = mock.Mock()
    repo.editar_tipo_bem.return_value = tipo_bem
    result = editar_tipo_bem_usecase(tipo_bem["id"], tipo_bem["descricao"], repo)

    repo.editar_tipo_bem.assert_called_with(tipo_bem["id"], tipo_bem["descricao"])

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_bem


def test_remover_tipo_bem_usecase(tipo_bem):
    repo = mock.Mock()
    repo.remover_tipo_bem.return_value = tipo_bem
    result = remover_tipo_bem_usecase(tipo_bem["id"], repo)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_bem

