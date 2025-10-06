from datetime import date, datetime
import pytest

from core.types import ResultSuccess
from emprestimo.domain.contracts.mail import MailService
from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.repositories.contracts import EmprestimoRepository
from emprestimo.usecases import NotificarDevolucaoUsecase
from unittest.mock import Mock

from ensino.domain.entities import AlunoEntity
from ensino.repositories.contracts import AlunoRepository


@pytest.fixture
def data_devolucao():
    return date(2025, 9, 25)


@pytest.fixture
def emprestimo(data_devolucao):
    return EmprestimoEntity(
        id=1,
        data_emprestimo="2025-09-01",
        data_devolucao_prevista=data_devolucao,
        data_devolucao=None,
        estado=EmprestimoEstadoEnum.ATIVO,
        bem_id=1,
        aluno_id=1,
    )


@pytest.fixture
def aluno():
    return AlunoEntity(
        id=1,
        nome="João da Silva",
        cpf="12345678901",
        email="joao.silva@ifpr.edu.br",
        matricula="2025001",
        telefone="41999990001",
        forma_selecao_id=1,
        curso_id=1,
    )


def test_notificacao_devolucao_envia_email(
    emprestimo, aluno: AlunoEntity, data_devolucao
):
    mail_service = Mock(spec=MailService)
    emprestimo_repo = Mock(spec=EmprestimoRepository)
    aluno_repo = Mock(spec=AlunoRepository)

    aluno_repo.buscar_por_id.return_value = aluno
    emprestimo_repo.listar_emprestimos_devolucao_proxima.return_value = [emprestimo]

    mail_service.enviar_email.return_value = 1

    usecase = NotificarDevolucaoUsecase(emprestimo_repo, aluno_repo, mail_service)
    result = usecase.execute(data_devolucao)

    assert isinstance(result, ResultSuccess)
    assert aluno.email in result.value.keys()
    assert result.value[aluno.email] == 1
