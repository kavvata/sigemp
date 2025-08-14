from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from ensino.domain.entities import CampusEntity
from ensino.usecases import CadastrarCampusUsecase, ListarCampiUsecase


@pytest.fixture
def campus():
    return CampusEntity(sigla="PNG", nome="Paranaguá")


@pytest.fixture
def lista_campi():
    return [
        CampusEntity(sigla="PNG", nome="Paranaguá"),
        CampusEntity(sigla="CWB", nome="Curitiba"),
        CampusEntity(sigla="CSV", nome="Cascavel"),
        CampusEntity(sigla="CLB", nome="Colombo"),
        CampusEntity(sigla="LND", nome="Londrina"),
    ]


def test_listar_campi(lista_campi):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_campi.return_value = lista_campi
    policy.pode_listar.return_value = True

    usecase = ListarCampiUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_campi.assert_called()
    policy.pode_listar.assert_called()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_campi


def test_nao_pode_listar_campi(lista_campi):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_campi.return_value = lista_campi
    policy.pode_listar.return_value = False

    usecase = ListarCampiUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_bens.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_campus(campus):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.cadastrar_campus.return_value = campus
    policy.pode_criar.return_value = True

    usecase = CadastrarCampusUsecase(repo, policy)
    result = usecase.execute(campus)

    repo.cadastrar_campus.assert_called_with(campus, policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == campus


def test_nao_pode_cadastrar_campus(campus):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.cadastrar_campus.return_value = campus
    policy.pode_criar.return_value = False

    usecase = CadastrarCampusUsecase(repo, policy)
    result = usecase.execute(campus)

    repo.cadastrar_campus.assert_not_called()
    assert isinstance(result, ResultError)


def test_editar_campus(campus):
    raise NotImplementedError


def test_remover_campus(campus):
    raise NotImplementedError


def test_nao_pode_remover_campus(campus):
    raise NotImplementedError
