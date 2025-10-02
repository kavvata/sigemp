from datetime import date
from unittest import mock
import pytest

from core.types import ResultError, ResultSuccess
from emprestimo.domain.entities import OcorrenciaEntity
from emprestimo.policies.contracts import OcorrenciaPolicy
from emprestimo.repositories.contracts import OcorrenciaRepository
from tests.emprestimo.test_emprestimo_usecases import emprestimo  # pyright: ignore[reportUnusedImport]  # noqa: F401
from tests.patrimonio.test_bem_usecases import bem  # noqa: F401  # pyright: ignore[reportUnusedImport]
from tests.ensino.test_aluno_usecases import aluno  # noqa: F401  # pyright: ignore[reportUnusedImport]


from emprestimo.usecases import (
    ListarOcorrenciasUsecase,
    ListarOcorrenciasBemUsecase,
    ListarOcorrenciasAlunoUsecase,
    ListarOcorrenciasEmprestimoUsecase,
    RegistrarOcorrenciaUsecase,
    CancelarOcorrenciaUsecase,
)


@pytest.fixture
def mock_repo():
    return mock.Mock(spec=OcorrenciaRepository)


@pytest.fixture
def mock_policy():
    policy = mock.Mock(spec=OcorrenciaPolicy)
    policy.user = mock.Mock()
    return policy


@pytest.fixture
def ocorrencia():
    return OcorrenciaEntity(
        id=1,
        data_ocorrencia=date(2025, 10, 1),
        emprestimo_id=1,
        tipo_id=1,
        tipo_descricao="Quebra",
    )


@pytest.fixture
def ocorrencia_cancelada(ocorrencia):
    ocorrencia.cancelado_em = date(2025, 10, 2)
    ocorrencia.cancelado_por_id = 1
    ocorrencia.motivo_cancelamento = "Registro duplicado"
    return ocorrencia


@pytest.fixture
def lista_ocorrencias():
    return [
        OcorrenciaEntity(
            id=i,
            data_ocorrencia=date(2025, 10, 1),
            emprestimo_id=1,
            tipo_id=i,
            tipo_descricao=f"Tipo {i}",
        )
        for i in range(1, 5)
    ]


def test_listar_ocorrencias_usecase(mock_repo, mock_policy, lista_ocorrencias):
    mock_policy.pode_listar.return_value = True
    mock_repo.listar_ocorrencias.return_value = lista_ocorrencias

    usecase = ListarOcorrenciasUsecase(mock_repo, mock_policy)
    result = usecase.execute()

    mock_policy.pode_listar.assert_called_once()
    mock_repo.listar_ocorrencias.assert_called_once()
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_ocorrencias


def test_listar_ocorrencias_sem_permissao_usecase(
    mock_repo, mock_policy, lista_ocorrencias
):
    mock_policy.pode_listar.return_value = False

    usecase = ListarOcorrenciasUsecase(mock_repo, mock_policy)
    result = usecase.execute()

    mock_policy.pode_listar.assert_called_once()
    mock_repo.listar_ocorrencias.assert_not_called()
    assert isinstance(result, ResultError)
    assert "permissão" in result.mensagem.lower()


def test_listar_ocorrencias_do_bem_usecase(
    mock_repo, mock_policy, bem, lista_ocorrencias
):
    mock_policy.pode_listar.return_value = True
    mock_repo.listar_ocorrencias_do_bem.return_value = lista_ocorrencias

    usecase = ListarOcorrenciasBemUsecase(mock_repo, mock_policy)
    result = usecase.execute(bem.id)

    mock_policy.pode_listar.assert_called_once()
    mock_repo.listar_ocorrencias_do_bem.assert_called_once_with(bem.id)
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_ocorrencias


def test_listar_ocorrencias_do_aluno_usecase(
    mock_repo, mock_policy, aluno, lista_ocorrencias
):
    mock_policy.pode_listar.return_value = True
    mock_repo.listar_ocorrencias_do_aluno.return_value = lista_ocorrencias

    usecase = ListarOcorrenciasAlunoUsecase(mock_repo, mock_policy)
    result = usecase.execute(aluno.id)

    mock_policy.pode_listar.assert_called_once()
    mock_repo.listar_ocorrencias_do_aluno.assert_called_once_with(aluno.id)
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_ocorrencias


def test_listar_ocorrencias_do_emprestimo_usecase(
    mock_repo, mock_policy, emprestimo, lista_ocorrencias
):
    mock_policy.pode_listar.return_value = True
    mock_repo.listar_ocorrencias_do_emprestimo.return_value = lista_ocorrencias

    usecase = ListarOcorrenciasEmprestimoUsecase(mock_repo, mock_policy)
    result = usecase.execute(emprestimo.id)

    mock_policy.pode_listar.assert_called_once()
    mock_repo.listar_ocorrencias_do_emprestimo.assert_called_once_with(emprestimo.id)
    assert isinstance(result, ResultSuccess)
    assert result.value == lista_ocorrencias


def test_registrar_ocorrencia_usecase(mock_repo, mock_policy, ocorrencia):
    mock_policy.pode_criar.return_value = True
    mock_repo.cadastrar_ocorrencia.return_value = ocorrencia

    usecase = RegistrarOcorrenciaUsecase(mock_repo, mock_policy)
    result = usecase.execute(ocorrencia)

    mock_policy.pode_criar.assert_called_once()
    mock_repo.cadastrar_ocorrencia.assert_called_once_with(ocorrencia, mock_policy.user)
    assert isinstance(result, ResultSuccess)
    assert result.value == ocorrencia


def test_registrar_ocorrencia_sem_permissao_usecase(mock_repo, mock_policy, ocorrencia):
    mock_policy.pode_criar.return_value = False

    usecase = RegistrarOcorrenciaUsecase(mock_repo, mock_policy)
    result = usecase.execute(ocorrencia)

    mock_policy.pode_criar.assert_called_once()
    mock_repo.cadastrar_ocorrencia.assert_not_called()
    assert isinstance(result, ResultError)
    assert "permissão" in result.mensagem.lower()


def test_cancelar_ocorrencia_usecase(mock_repo, mock_policy, ocorrencia):
    motivo = "Registro em duplicidade"
    mock_policy.pode_remover.return_value = True
    mock_repo.buscar_por_id.return_value = ocorrencia
    mock_repo.editar_ocorrencia.return_value = ocorrencia

    usecase = CancelarOcorrenciaUsecase(mock_repo, mock_policy)
    result = usecase.execute(ocorrencia.id, motivo)

    mock_policy.pode_remover.assert_called_once_with(ocorrencia)
    mock_repo.buscar_por_id.assert_called_once_with(ocorrencia.id)
    mock_repo.editar_ocorrencia.assert_called_once()
    assert isinstance(result, ResultSuccess)
    assert result.value.cancelado_em is not None
    assert result.value.motivo_cancelamento == motivo


def test_cancelar_ocorrencia_sem_permissao_usecase(mock_repo, mock_policy, ocorrencia):
    motivo = "Registro em duplicidade"
    mock_policy.pode_remover.return_value = False
    mock_repo.buscar_por_id.return_value = ocorrencia

    usecase = CancelarOcorrenciaUsecase(mock_repo, mock_policy)
    result = usecase.execute(ocorrencia.id, motivo)

    mock_policy.pode_remover.assert_called_once_with(ocorrencia)
    mock_repo.buscar_por_id.assert_called_once_with(ocorrencia.id)
    mock_repo.editar_ocorrencia.assert_not_called()
    assert isinstance(result, ResultError)
    assert "permissão" in result.mensagem.lower()


def test_cancelar_ocorrencia_ja_cancelada_usecase(
    mock_repo, mock_policy, ocorrencia_cancelada
):
    motivo = "Novo motivo"
    mock_policy.pode_remover.return_value = True
    mock_repo.buscar_por_id.return_value = ocorrencia_cancelada

    usecase = CancelarOcorrenciaUsecase(mock_repo, mock_policy)
    result = usecase.execute(ocorrencia_cancelada.id, motivo)

    mock_policy.pode_remover.assert_called_once_with(ocorrencia_cancelada)
    mock_repo.buscar_por_id.assert_called_once_with(ocorrencia_cancelada.id)
    mock_repo.editar_ocorrencia.assert_not_called()
    assert isinstance(result, ResultError)
    assert "cancelada" in result.mensagem.lower()


def test_cancelar_ocorrencia_nao_encontrada_usecase(mock_repo, mock_policy):
    motivo = "Registro em duplicidade"
    mock_policy.pode_remover.return_value = True
    mock_repo.buscar_por_id.return_value = None

    usecase = CancelarOcorrenciaUsecase(mock_repo, mock_policy)
    result = usecase.execute(999, motivo)

    mock_policy.pode_remover.assert_not_called()
    mock_repo.buscar_por_id.assert_called_once_with(999)
    mock_repo.editar_ocorrencia.assert_not_called()
    assert isinstance(result, ResultError)
    assert "não encontrada" in result.mensagem.lower()
