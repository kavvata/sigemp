from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from emprestimo.domain.entities import TipoOcorrenciaEntity
from emprestimo.usecases import (
    ListarTiposOcorrenciaUsecase,
    CadastrarTipoOcorrenciaUsecase,
    EditarTipoOcorrenciaUsecase,
    RemoverTipoOcorrenciaUsecase,
)


@pytest.fixture
def tipo_ocorrencia():
    return TipoOcorrenciaEntity(id=1, descricao="Perda")


@pytest.fixture
def lista_tipos_ocorrencia():
    return [
        TipoOcorrenciaEntity(id=1, descricao="Perda"),
        TipoOcorrenciaEntity(id=2, descricao="Roubo"),
        TipoOcorrenciaEntity(id=3, descricao="Extravio"),
        TipoOcorrenciaEntity(id=4, descricao="Dano"),
    ]


def test_listar_tipos_ocorrencia(lista_tipos_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_tipos_ocorrencia.return_value = lista_tipos_ocorrencia
    policy.pode_listar.return_value = True

    usecase = ListarTiposOcorrenciaUsecase(repo, policy)

    if usecase.pode_listar():
        result = usecase.execute()

    repo.listar_tipos_ocorrencia.assert_called_with()
    policy.pode_listar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_tipos_ocorrencia


def test_nao_pode_listar_tipos_ocorrencia_usecase(lista_tipos_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_tipos_ocorrencia.return_value = lista_tipos_ocorrencia
    policy.pode_listar.return_value = False

    usecase = ListarTiposOcorrenciaUsecase(repo, policy)

    result = usecase.execute()

    repo.listar_tipos_ocorrencia.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_tipo_ocorrencia_usecase(tipo_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_tipo_ocorrencia.return_value = tipo_ocorrencia
    policy.pode_criar.return_value = True
    policy.user = user

    usecase = CadastrarTipoOcorrenciaUsecase(repo, policy)

    if usecase.pode_criar():
        result = usecase.execute(tipo_ocorrencia)

    repo.cadastrar_tipo_ocorrencia.assert_called_with(tipo_ocorrencia, user)
    policy.pode_criar.assert_called_with()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_ocorrencia


def test_nao_pode_cadastrar_tipo_ocorrencia_usecase(tipo_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.cadastrar_tipo_ocorrencia.return_value = tipo_ocorrencia
    policy.pode_criar.return_value = False
    policy.user = user

    usecase = CadastrarTipoOcorrenciaUsecase(repo, policy)

    result = usecase.execute(tipo_ocorrencia)

    repo.cadastrar_tipo_ocorrencia.assert_not_called()
    policy.pode_criar.assert_called()

    assert not result
    assert isinstance(result, ResultError)


def test_editar_tipo_ocorrencia_usecase(tipo_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = tipo_ocorrencia
    repo.editar_tipo_ocorrencia.return_value = tipo_ocorrencia
    policy.pode_editar.return_value = True
    policy.user = user

    usecase = EditarTipoOcorrenciaUsecase(repo, policy)

    result = usecase.get_tipo_ocorrencia(tipo_ocorrencia.id)
    encontrado = result.value

    assert encontrado

    result = usecase.execute(encontrado)

    repo.buscar_por_id.assert_called_with(tipo_ocorrencia.id)
    repo.editar_tipo_ocorrencia.assert_called_with(encontrado, user)
    policy.pode_editar.assert_called_with(tipo_ocorrencia)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_ocorrencia


def test_nao_pode_editar_tipo_ocorrencia_usecase(tipo_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = tipo_ocorrencia
    repo.editar_tipo_ocorrencia.return_value = tipo_ocorrencia
    policy.pode_editar.return_value = False
    policy.user = user

    usecase = EditarTipoOcorrenciaUsecase(repo, policy)

    result = usecase.get_tipo_ocorrencia(tipo_ocorrencia.id)
    assert not result
    assert isinstance(result, ResultError)

    result = usecase.execute(tipo_ocorrencia)

    repo.buscar_por_id.assert_called_with(tipo_ocorrencia.id)
    repo.editar_tipo_ocorrencia.assert_not_called()
    policy.pode_editar.assert_called_with(tipo_ocorrencia)

    assert not result
    assert isinstance(result, ResultError)


def test_remover_tipo_ocorrencia_usecase(tipo_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = tipo_ocorrencia
    repo.remover_tipo_ocorrencia.return_value = tipo_ocorrencia
    policy.pode_remover.return_value = True
    policy.user = user

    usecase = RemoverTipoOcorrenciaUsecase(repo, policy)

    result = usecase.execute(tipo_ocorrencia.id)

    repo.remover_tipo_ocorrencia.assert_called_with(tipo_ocorrencia.id, user)
    policy.pode_remover.assert_called_with(tipo_ocorrencia)

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == tipo_ocorrencia


def test_nao_pode_remover_tipo_ocorrencia_usecase(tipo_ocorrencia):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    repo.buscar_por_id.return_value = tipo_ocorrencia
    repo.remover_tipo_ocorrencia.return_value = tipo_ocorrencia
    policy.pode_remover.return_value = False
    policy.user = user

    usecase = RemoverTipoOcorrenciaUsecase(repo, policy)

    result = usecase.execute(tipo_ocorrencia.id)

    repo.remover_tipo_ocorrencia.assert_not_called()
    policy.pode_remover.assert_called_with(tipo_ocorrencia)

    assert not result
    assert isinstance(result, ResultError)
