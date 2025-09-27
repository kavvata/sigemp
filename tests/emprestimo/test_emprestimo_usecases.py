from io import BytesIO
from unittest import mock
from datetime import date
import pytest

from core.types import ResultError, ResultSuccess
from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.services.contracts import PDFService
from emprestimo.usecases import (
    ListarEmprestimosUsecase,
    CadastrarEmprestimoUsecase,
    EditarEmprestimoUsecase,
    RemoverEmprestimoUsecase,
    GerarTermoResponsabilidadeUsecase,
    GerarTermoDevolucaoUsecase,
    RegistrarDevolucaoEmprestimoUsecase,
)


@pytest.fixture
def mock_pdf_service():
    return mock.Mock(spec=PDFService)


@pytest.fixture
def mock_emprestimo_repo():
    return mock.Mock()


@pytest.fixture
def mock_policy():
    policy = mock.Mock()
    policy.user = mock.Mock()
    return policy


@pytest.fixture
def emprestimo():
    return EmprestimoEntity(
        id=1,
        data_emprestimo="2025-09-01",
        data_devolucao_prevista="2025-09-15",
        data_devolucao=None,
        estado=EmprestimoEstadoEnum.ATIVO,
        bem_id=1,
        aluno_id=1,
    )


@pytest.fixture
def lista_emprestimos_em_andamento():
    return [
        EmprestimoEntity(
            id=i,
            data_emprestimo="2025-09-01",
            data_devolucao_prevista="2025-09-15",
            data_devolucao=None,
            estado=EmprestimoEstadoEnum.ATIVO,
            bem_id=i,
            aluno_id=1,
        )
        for i in range(1, 5)
    ]


def test_listar_emprestimos(lista_emprestimos_em_andamento):
    repo = mock.Mock()
    policy = mock.Mock()

    repo.listar_emprestimos.return_value = lista_emprestimos_em_andamento
    policy.pode_listar.return_value = True

    usecase = ListarEmprestimosUsecase(repo, policy)
    result = usecase.execute()

    repo.listar_emprestimos.assert_called()
    policy.pode_listar.assert_called()

    assert isinstance(result, ResultSuccess)
    assert result.value == lista_emprestimos_em_andamento


def test_nao_pode_listar_emprestimos_usecase(lista_emprestimos_em_andamento):
    repo = mock.Mock()
    policy = mock.Mock()

    policy.pode_listar.return_value = False
    usecase = ListarEmprestimosUsecase(repo, policy)
    result = usecase.execute()

    policy.pode_listar.assert_called()
    assert isinstance(result, ResultError)


def test_cadastrar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    repo.buscar_ativo_por_bem.return_value = None
    repo.buscar_ativos_por_aluno.return_value = []
    repo.cadastrar_emprestimo.return_value = emprestimo
    policy.pode_criar.return_value = True

    usecase = CadastrarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    repo.buscar_ativo_por_bem.assert_called_with(emprestimo.bem_id)
    repo.buscar_ativos_por_aluno.assert_called_with(emprestimo.aluno_id)
    repo.cadastrar_emprestimo.assert_called_with(emprestimo, user)

    assert isinstance(result, ResultSuccess)
    assert result.value == emprestimo


def test_nao_pode_cadastrar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    repo.buscar_ativo_por_bem.return_value = None
    repo.buscar_ativos_por_aluno.return_value = []
    repo.cadastrar_emprestimo.return_value = emprestimo
    policy.pode_criar.return_value = False

    usecase = CadastrarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    repo.buscar_ativo_por_bem.assert_not_called()
    repo.buscar_ativos_por_aluno.assert_not_called()
    repo.cadastrar_emprestimo.assert_not_called()

    assert isinstance(result, ResultError)


def test_nao_pode_cadastrar_emprestimo_quando_aluno_tem_ativo(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_criar.return_value = True

    repo.buscar_ativo_por_bem.return_value = None
    repo.buscar_ativos_por_aluno.return_value = [
        mock.Mock(estado=EmprestimoEstadoEnum.ATIVO)
    ]
    usecase = CadastrarEmprestimoUsecase(repo, policy)

    result = usecase.execute(emprestimo)

    repo.buscar_ativo_por_bem.assert_called_with(emprestimo.bem_id)
    repo.buscar_ativos_por_aluno.assert_called_with(emprestimo.aluno_id)
    assert isinstance(result, ResultError)


def test_registrar_devolucao_emprestimo_usecase():
    emprestimo = EmprestimoEntity(
        data_emprestimo=date(2025, 9, 1),
        data_devolucao_prevista=date(2025, 9, 15),
        data_devolucao=None,
        estado=EmprestimoEstadoEnum.ATIVO,
        bem_id=1,
        aluno_id=1,
    )

    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_editar.return_value = True

    def registrar_devolucao_mock(e, _user):
        e.data_devolucao = date.today()
        e.estado = EmprestimoEstadoEnum.FINALIZADO
        return e

    repo.registrar_devolucao.side_effect = registrar_devolucao_mock

    usecase = RegistrarDevolucaoEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    print(result)

    repo.registrar_devolucao.assert_called_with(emprestimo, user)
    assert isinstance(result, ResultSuccess)
    assert result.value.data_devolucao is not None
    assert result.value.estado == EmprestimoEstadoEnum.FINALIZADO


def test_nao_pode_registrar_devolucao_emprestimo_ja_devolvido_usecase():
    emprestimo = EmprestimoEntity(
        data_emprestimo=date(2025, 9, 1),
        data_devolucao_prevista=date(2025, 9, 15),
        data_devolucao=date(2025, 9, 10),
        estado=EmprestimoEstadoEnum.FINALIZADO,
        bem_id=1,
        aluno_id=1,
    )

    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user
    policy.pode_editar.return_value = True

    # Registrar devolução deve retornar um erro se já devolvido
    def registrar_devolucao_mock(e):
        if e.data_devolucao is not None:
            raise ValueError("Empréstimo já devolvido")
        e.data_devolucao = date.today()
        e.estado = EmprestimoEstadoEnum.FINALIZADO
        return e

    repo.registrar_devolucao.side_effect = registrar_devolucao_mock

    usecase = RegistrarDevolucaoEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    repo.registrar_devolucao.assert_called_with(emprestimo, user)
    assert isinstance(result, ResultError)


def test_editar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    policy.pode_editar.return_value = True
    repo.buscar_por_id.return_value = emprestimo
    repo.editar_emprestimo.return_value = emprestimo

    usecase = EditarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    repo.buscar_por_id.assert_called_with(emprestimo.id)
    repo.editar_emprestimo.assert_called_with(emprestimo, user)

    assert isinstance(result, ResultSuccess)
    assert result.value == emprestimo


def test_nao_pode_editar_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_editar.return_value = False

    usecase = EditarEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo)

    policy.pode_editar.assert_called()
    assert isinstance(result, ResultError)


def test_remover_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    user = mock.Mock()
    policy.user = user

    policy.pode_remover.return_value = True
    repo.buscar_por_id.return_value = emprestimo

    usecase = RemoverEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo.id)

    repo.buscar_por_id.assert_called_with(emprestimo.id)
    repo.remover_emprestimo.assert_called_with(emprestimo.id, user)

    assert isinstance(result, ResultSuccess)


def test_nao_pode_remover_emprestimo_usecase(emprestimo):
    repo = mock.Mock()
    policy = mock.Mock()
    policy.pode_remover.return_value = False

    usecase = RemoverEmprestimoUsecase(repo, policy)
    result = usecase.execute(emprestimo.id)

    policy.pode_remover.assert_called()
    assert isinstance(result, ResultError)


def test_gerar_termo_responsabilidade_usecase_sucesso(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = True

    pdf_content = BytesIO(b"termo de responsabilidade")
    mock_pdf_service.gerar_termo_responsabilidade.return_value = pdf_content

    usecase = GerarTermoResponsabilidadeUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_responsabilidade.assert_called_once_with(
        emprestimo, mock_policy.user
    )
    assert isinstance(result, ResultSuccess)
    assert result.value == pdf_content


def test_gerar_termo_responsabilidade_usecase_sem_permissao(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = False

    usecase = GerarTermoResponsabilidadeUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_responsabilidade.assert_not_called()
    assert isinstance(result, ResultError)


def test_nao_pode_gerar_termo_responsabilidade_emprestimo_finalizado(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = True
    emprestimo_finalizado: EmprestimoEntity = emprestimo
    emprestimo_finalizado.data_devolucao = date(2025, 9, 25)
    emprestimo_finalizado.estado = EmprestimoEstadoEnum.FINALIZADO

    usecase = GerarTermoResponsabilidadeUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo_finalizado)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_responsabilidade.assert_not_called()
    assert isinstance(result, ResultError)


def test_gerar_termo_responsabilidade_usecase_erro_pdf_service(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = True
    mock_pdf_service.gerar_termo_responsabilidade.side_effect = Exception(
        "Erro ao gerar PDF"
    )

    usecase = GerarTermoResponsabilidadeUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_responsabilidade.assert_called_once_with(
        emprestimo, mock_policy.user
    )
    assert isinstance(result, ResultError)
    assert "Erro ao gerar PDF" in result.mensagem


def test_gerar_termo_devolucao_usecase_sucesso(
    emprestimo: EmprestimoEntity, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = True

    emprestimo.estado = EmprestimoEstadoEnum.FINALIZADO
    emprestimo.data_devolucao = date(2025, 9, 25)

    pdf_content = BytesIO(b"Termo de devolucao")
    mock_pdf_service.gerar_termo_devolucao.return_value = pdf_content

    usecase = GerarTermoDevolucaoUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_devolucao.assert_called_once_with(
        emprestimo, mock_policy.user
    )
    assert isinstance(result, ResultSuccess)
    assert result.value == pdf_content


def test_gerar_termo_devolucao_usecase_sem_permissao(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = False

    usecase = GerarTermoDevolucaoUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_devolucao.assert_not_called()
    assert isinstance(result, ResultError)


def test_gerar_termo_devolucao_usecase_erro_pdf_service(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = True
    mock_pdf_service.gerar_termo_devolucao.side_effect = Exception(
        "Erro ao gerar PDF de devolução"
    )

    emprestimo.estado = EmprestimoEstadoEnum.FINALIZADO
    emprestimo.data_devolucao = date(2025, 9, 25)

    usecase = GerarTermoDevolucaoUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_devolucao.assert_called_once_with(
        emprestimo, mock_policy.user
    )
    assert isinstance(result, ResultError)
    assert "Erro ao gerar PDF" in result.mensagem


def test_gerar_termo_devolucao_requer_emprestimo_finalizado(
    emprestimo, mock_emprestimo_repo, mock_policy, mock_pdf_service
):
    mock_policy.pode_gerar_termos.return_value = True
    emprestimo_nao_finalizado = emprestimo
    emprestimo_nao_finalizado.data_devolucao = None

    usecase = GerarTermoDevolucaoUsecase(
        mock_emprestimo_repo, mock_policy, mock_pdf_service
    )
    result = usecase.execute(emprestimo_nao_finalizado)

    mock_policy.pode_gerar_termos.assert_called_once()
    mock_pdf_service.gerar_termo_devolucao.assert_not_called()
    assert isinstance(result, ResultError)
