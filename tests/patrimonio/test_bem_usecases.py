from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from patrimonio.usecases import (
    ListarBensUsecase,
    CadastrarBemUsecase,
    EditarBemUsecase,
    RemoverBemUsecase,
)

from patrimonio.domain.entities import BemEntity


@pytest.fixture
def bem():
    return BemEntity(
        id=1,
        patrimonio="000.000.000.000",
        descricao="Projetor Epson X1000",
        tipo_id=1,
        grau_fragilidade_id=2,
        estado_conservacao_id=1,
        marca_modelo_id=1,
    )


@pytest.fixture
def lista_bem():
    return [
        BemEntity(
            id=1,
            patrimonio="000.000.000.000",
            descricao="Projetor Epson X1000",
            tipo_id=1,
            grau_fragilidade_id=2,
            estado_conservacao_id=1,
            marca_modelo_id=1,
        ),
        BemEntity(
            id=2,
            patrimonio="000.000.000.001",
            descricao="Notebook Dell Latitude",
            tipo_id=2,
            grau_fragilidade_id=1,
            estado_conservacao_id=2,
            marca_modelo_id=2,
        ),
        BemEntity(
            id=3,
            patrimonio="000.000.000.002",
            descricao="Centrífuga de bancada",
            tipo_id=3,
            grau_fragilidade_id=3,
            estado_conservacao_id=3,
            marca_modelo_id=3,
        ),
    ]


def test_listar_bens_usecase(lista_bem):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_bens.return_value = lista_bem
    policy.pode_listar.return_value = True

    usecase = ListarBensUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_bens.assert_called()
    policy.pode_listar.assert_called()

    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_bem


def test_nao_pode_listar_bens_sem_permissao_usecase(lista_bem):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_bens.return_value = lista_bem
    policy.pode_listar.return_value = False

    usecase = ListarBensUsecase(repo, policy)

    result = usecase.execute()

    repo.listar_bens.assert_not_called()
    policy.pode_listar.assert_called_with()

    assert not result
    assert isinstance(result, ResultError)


def test_cadastrar_bem_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_criar.return_value = True
    repo.buscar_por_patrimonio.return_value = None
    repo.cadastrar_bem.return_value = bem

    usecase = CadastrarBemUsecase(repo, policy)

    result = usecase.execute(bem)

    repo.buscar_por_patrimonio.assert_called_with(bem.patrimonio)
    repo.cadastrar_bem.assert_called_with(
        bem,
        user,
    )
    assert isinstance(result, ResultSuccess)
    assert result.value == bem


def test_nao_pode_cadastrar_bem_sem_permissao_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_criar.return_value = False
    policy.user = mock.Mock()

    usecase = CadastrarBemUsecase(repo, policy)
    result = usecase.execute(bem)

    repo.cadastrar_bem.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_cadastrar_bem_com_patrimonio_existente_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_criar.return_value = True
    repo.buscar_por_patrimonio.return_value = bem  # já existe

    usecase = CadastrarBemUsecase(repo, policy)
    result = usecase.execute(bem)

    repo.cadastrar_bem.assert_not_called()
    assert isinstance(result, ResultError)


def test_editar_bem_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_editar.return_value = True
    repo.buscar_por_id.return_value = bem
    repo.buscar_por_patrimonio.return_value = None
    repo.editar_bem.return_value = bem

    usecase = EditarBemUsecase(repo, policy)
    result = usecase.execute(bem)

    assert isinstance(result, ResultSuccess)
    assert result.value == bem


def test_nao_pode_editar_bem_sem_permissao_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_editar.return_value = False
    repo.buscar_por_id.return_value = bem

    usecase = EditarBemUsecase(repo, policy)
    result = usecase.execute(bem)

    repo.editar_bem.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_editar_para_patrimonio_existente_usecase(bem, lista_bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_editar.return_value = True
    repo.buscar_por_id.return_value = bem
    repo.buscar_por_patrimonio.return_value = lista_bem[1]

    usecase = EditarBemUsecase(repo, policy)
    bem.patirmonio = lista_bem[1].patrimonio
    result = usecase.execute(bem)

    repo.editar_bem.assert_not_called()
    assert isinstance(result, ResultError)


def test_remover_bem_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_remover.return_value = True
    repo.buscar_por_id.return_value = bem
    repo.remover_bem.return_value = bem

    usecase = RemoverBemUsecase(repo, policy)
    result = usecase.execute(bem.id)

    repo.remover_bem.assert_called_with(bem.id, user)
    assert isinstance(result, ResultSuccess)
    assert result.value == bem


def test_nao_pode_remover_bem_sem_permissao_usecase(bem):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_remover.return_value = False
    repo.buscar_por_id.return_value = bem

    usecase = RemoverBemUsecase(repo, policy)
    result = usecase.execute(bem.id)

    repo.remover_bem.assert_not_called()
    assert isinstance(result, ResultError)
