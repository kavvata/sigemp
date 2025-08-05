from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from patrimonio.usecases import (
    ListarMarcaModeloUsecase,
    CadastrarMarcaModeloUsecase,
    EditarMarcaModeloUsecase,
    RemoverMarcaModeloUsecase,
)

from patrimonio.domain.entities import MarcaModeloEntity


@pytest.fixture
def marca_modelo():
    return MarcaModeloEntity(id=1, marca="Epson", modelo="PowerLite X49")


@pytest.fixture
def lista_marca_modelo():
    return [
        MarcaModeloEntity(id=1, marca="Epson", modelo="PowerLite X49"),
        MarcaModeloEntity(id=2, marca="Dell", modelo="Latitude 5420"),
        MarcaModeloEntity(id=3, marca="Optika", modelo="B-150R"),
        MarcaModeloEntity(id=4, marca="Minipa", modelo="ET-1002"),
        MarcaModeloEntity(id=5, marca="Canon", modelo="EOS Rebel T7"),
    ]


def test_listar_marca_modelo(lista_marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_marca_modelo.return_value = lista_marca_modelo
    policy.pode_listar.return_value = True

    usecase = ListarMarcaModeloUsecase(repo, policy)

    if usecase.pode_listar():
        result = usecase.execute()

    repo.listar_marca_modelo.assert_called_with()
    policy.pode_listar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_marca_modelo


def test_nao_pode_listar_marca_modelo_usecase(lista_marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_marca_modelo.return_value = lista_marca_modelo
    policy.pode_listar.return_value = False

    usecase = ListarMarcaModeloUsecase(repo, policy)

    result = usecase.execute()

    repo.listar_marca_modelo.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_marca_modelo_usecase(marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_marca_modelo.return_value = marca_modelo
    policy.pode_criar.return_value = True
    policy.user = user

    usecase = CadastrarMarcaModeloUsecase(repo, policy)

    if usecase.pode_criar():
        result = usecase.execute(marca_modelo.marca, marca_modelo.modelo)

    repo.cadastrar_marca_modelo.assert_called_with(
        marca_modelo.marca, marca_modelo.modelo, user
    )
    policy.pode_criar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == marca_modelo


def test_nao_pode_cadastrar_marca_modelo_usecase(marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_marca_modelo.return_value = marca_modelo
    policy.pode_criar.return_value = False
    policy.user = user

    usecase = CadastrarMarcaModeloUsecase(repo, policy)

    result = usecase.execute(marca_modelo.marca, marca_modelo.modelo)

    repo.cadastrar_marca_modelo.assert_not_called()
    policy.pode_criar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_editar_marca_modelo_usecase(marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = marca_modelo
    repo.editar_marca_modelo.return_value = marca_modelo
    policy.pode_editar.return_value = True
    policy.user = user

    usecase = EditarMarcaModeloUsecase(repo, policy)

    result = usecase.get_marca_modelo(marca_modelo.id)
    encontrado = result.value

    assert encontrado

    result = usecase.execute(encontrado.id, encontrado.marca, encontrado.modelo)

    repo.buscar_por_id.assert_called_with(marca_modelo.id)
    repo.editar_marca_modelo.assert_called_with(
        marca_modelo.id,
        marca_modelo.marca,
        marca_modelo.modelo,
        user,
    )
    policy.pode_editar.assert_called_with(marca_modelo)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == marca_modelo


def test_nao_pode_editar_marca_modelo_usecase(marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = marca_modelo
    repo.editar_marca_modelo.return_value = marca_modelo
    policy.pode_editar.return_value = False
    policy.user = user

    usecase = EditarMarcaModeloUsecase(repo, policy)

    result = usecase.get_marca_modelo(marca_modelo.id)
    assert not result
    assert isinstance(result, ResultError)

    result = usecase.execute(
        marca_modelo.id,
        marca_modelo.marca,
        marca_modelo.modelo,
    )

    repo.buscar_por_id.assert_called_with(marca_modelo.id)
    repo.editar_marca_modelo.assert_not_called()
    policy.pode_editar.assert_called_with(marca_modelo)

    assert not result
    assert isinstance(result, ResultError)


def test_remover_marca_modelo_usecase(marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = marca_modelo
    repo.remover_marca_modelo.return_value = marca_modelo
    policy.pode_remover.return_value = True
    policy.user = user

    usecase = RemoverMarcaModeloUsecase(repo, policy)

    result = usecase.execute(marca_modelo.id)

    repo.remover_marca_modelo.assert_called_with(marca_modelo.id, user)
    policy.pode_remover.assert_called_with(marca_modelo)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == marca_modelo


def test_nao_pode_remover_marca_modelo_usecase(marca_modelo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = marca_modelo
    repo.remover_marca_modelo.return_value = marca_modelo
    policy.pode_remover.return_value = False
    policy.user = user

    usecase = RemoverMarcaModeloUsecase(repo, policy)

    result = usecase.execute(marca_modelo.id)

    repo.remover_marca_modelo.assert_not_called()
    policy.pode_remover.assert_called_with(marca_modelo)

    assert not result
    assert isinstance(result, ResultError)
