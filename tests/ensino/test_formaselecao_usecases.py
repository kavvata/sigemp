from datetime import datetime, timedelta
from unittest import mock

import pytest

from core.types import ResultError, ResultSuccess
from ensino.domain.entities import FormaSelecaoEntity
from ensino.usecases import (
    CadastrarFormaSelecaoUsecase,
    EditarFormaSelecaoUsecase,
    ListarFormasSelecaoUsecase,
    RemoverFormaSelecaoUsecase,
)


@pytest.fixture
def forma_selecao():
    base_date = datetime(2020, 1, 1)
    return FormaSelecaoEntity(
        descricao="Edital N°01/2020",
        periodo_inicio=base_date,
        periodo_fim=base_date + timedelta(days=180),
    )


@pytest.fixture
def lista_formas_selecao():
    base_date = datetime(2020, 1, 1)
    return [
        FormaSelecaoEntity(
            descricao="Edital N°01/2020",
            periodo_inicio=base_date,
            periodo_fim=base_date + timedelta(days=180),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°02/2020",
            periodo_inicio=base_date + timedelta(days=200),
            periodo_fim=base_date + timedelta(days=365),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°03/2021",
            periodo_inicio=base_date.replace(year=2021, month=3, day=15),
            periodo_fim=base_date.replace(year=2021, month=9, day=15),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°04/2021",
            periodo_inicio=base_date.replace(year=2021, month=10, day=1),
            periodo_fim=base_date.replace(year=2022, month=3, day=1),
        ),
        FormaSelecaoEntity(
            descricao="Edital N°05/2022",
            periodo_inicio=base_date.replace(year=2022, month=4, day=10),
            periodo_fim=base_date.replace(year=2023, month=4, day=10),
        ),
    ]


def test_listar_formas_selecao(lista_formas_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_formas_selecao.return_value = lista_formas_selecao
    policy.pode_listar.return_value = True

    usecase = ListarFormasSelecaoUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_formas_selecao.assert_called()
    policy.pode_listar.assert_called()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_formas_selecao


def test_nao_pode_listar_formas_selecao(lista_formas_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_formas_selecao.return_value = lista_formas_selecao
    policy.pode_listar.return_value = False

    usecase = ListarFormasSelecaoUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_formas_selecao.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_forma_selecao(forma_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.cadastrar_forma_selecao.return_value = forma_selecao
    policy.pode_criar.return_value = True

    usecase = CadastrarFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(forma_selecao)

    repo.cadastrar_forma_selecao.assert_called_with(forma_selecao, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == forma_selecao


def test_nao_pode_cadastrar_forma_selecao(forma_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.cadastrar_forma_selecao.return_value = forma_selecao
    policy.pode_criar.return_value = False

    usecase = CadastrarFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(forma_selecao)

    repo.cadastrar_forma_selecao.assert_not_called()
    assert isinstance(result, ResultError)


def test_editar_forma_selecao(forma_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_editar.return_value = True
    repo.buscar_por_id.return_value = forma_selecao
    repo.editar_forma_selecao.return_value = forma_selecao

    usecase = EditarFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(forma_selecao)

    repo.buscar_por_id.assert_called_with(forma_selecao.id)
    repo.editar_forma_selecao.assert_called_with(forma_selecao, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == forma_selecao


def test_nao_pode_editar_forma_selecao(forma_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_editar.return_value = False
    repo.buscar_por_id.return_value = forma_selecao
    repo.editar_forma_selecao.return_value = forma_selecao

    usecase = EditarFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(forma_selecao)

    repo.editar_forma_selecao.assert_not_called()
    assert isinstance(result, ResultError)


def test_remover_forma_selecao(forma_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_remover.return_value = True
    repo.buscar_por_id.return_value = forma_selecao
    repo.remover_forma_selecao.return_value = forma_selecao

    usecase = RemoverFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(forma_selecao.id)

    repo.remover_forma_selecao.assert_called_with(forma_selecao.id, policy.user)
    assert isinstance(result, ResultSuccess)


def test_nao_pode_remover_forma_selecao(forma_selecao):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_remover.return_value = False
    repo.buscar_por_id.return_value = forma_selecao
    repo.remover_forma_selecao.return_value = forma_selecao

    usecase = RemoverFormaSelecaoUsecase(repo, policy)
    result = usecase.execute(forma_selecao.id)

    repo.remover_forma_selecao.assert_not_called()
    assert isinstance(result, ResultError)
