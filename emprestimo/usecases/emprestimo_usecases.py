from datetime import date
from typing import Optional
from core.types import ResultError, ResultSuccess
from emprestimo.domain.contracts.mail import MailService
from emprestimo.domain.entities import EmprestimoEntity
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.policies.contracts import EmprestimoPolicy
from emprestimo.repositories.contracts import EmprestimoRepository
from emprestimo.infrastructure.services.contracts import PDFService
from ensino.repositories.contracts import AlunoRepository
from sigemp import settings


class ListarEmprestimosUsecase:
    def __init__(self, repo: EmprestimoRepository, policy: EmprestimoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_listar(self):
        return self.policy.pode_listar()

    def execute(self):
        if not self.policy.pode_listar():
            return ResultError("Você não tem permissão para listar empréstimo.")

        try:
            resposta = self.repo.listar_emprestimos()
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao listar empréstimo: {e}")


class CadastrarEmprestimoUsecase:
    def __init__(self, repo: EmprestimoRepository, policy: EmprestimoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_criar(self):
        return self.policy.pode_criar()

    def execute(self, novo_emprestimo: EmprestimoEntity):
        if not self.policy.pode_criar():
            return ResultError("Você não tem permissão para cadastrar empréstimo")

        try:
            existente: Optional[EmprestimoEntity] = self.repo.buscar_ativo_por_bem(
                novo_emprestimo.bem_id
            )
            if existente:
                return ResultError(f"Bem Possui empréstimo ativo: {existente.id}")
        except Exception as e:
            return ResultError(f"Erro ao cadastrar empréstimo: {e}")

        try:
            existentes = self.repo.buscar_ativos_por_aluno(novo_emprestimo.aluno_id)
            if existentes:
                return ResultError(f"Aluno Possui empréstimos ativos: {existente.id}")
        except Exception as e:
            return ResultError(f"Erro ao cadastrar empréstimo: {e}")

        try:
            resposta = self.repo.cadastrar_emprestimo(
                novo_emprestimo,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao cadastrar empréstimo: {e}")


class RegistrarDevolucaoEmprestimoUsecase:
    def __init__(self, repo: EmprestimoRepository, policy: EmprestimoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self):
        return self.policy.pode_editar()

    def execute(self, emprestimo: EmprestimoEntity):
        if not self.policy.pode_editar(emprestimo):
            return ResultError(
                "Você não tem permissão para registrar devolução de empréstimo"
            )

        if (
            emprestimo.estado == EmprestimoEstadoEnum.FINALIZADO
            or emprestimo.data_devolucao is not None
            or emprestimo.devolucao_ciente_por_id is not None
        ):
            return ResultError(
                "Não é possível registrar devolução de empréstimo já devolvido."
            )

        try:
            resposta = self.repo.registrar_devolucao(
                emprestimo,
                self.policy.user,
            )
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao registrar devolução de empréstimo: {e}")


class EditarEmprestimoUsecase:
    def __init__(self, repo: EmprestimoRepository, policy: EmprestimoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def pode_editar(self, emprestimo):
        return self.policy.pode_editar(emprestimo)

    def get_emprestimo(self, id: int):
        try:
            emprestimo = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar emprestimo: {e}")

        if not self.policy.pode_editar(emprestimo):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(emprestimo)

    def execute(self, emprestimo: EmprestimoEntity):
        if not self.policy.pode_editar(emprestimo):
            return ResultError("Você não tem permissão para editar empréstimo.")

        resultado_busca_por_id = self.get_emprestimo(emprestimo.id)
        if not resultado_busca_por_id:
            return resultado_busca_por_id

        try:
            resposta = self.repo.editar_emprestimo(emprestimo, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao editar empréstimo: {e}")


class RemoverEmprestimoUsecase:
    def __init__(self, repo: EmprestimoRepository, policy: EmprestimoPolicy) -> None:
        self.repo = repo
        self.policy = policy

    def get_emprestimo(self, id: int):
        try:
            emprestimo = self.repo.buscar_por_id(id)
        except Exception as e:
            return ResultError(f"Erro ao buscar empréstimo: {e}")

        if not self.policy.pode_remover(emprestimo):
            return ResultError("Você não tem permissão para realizar esta ação.")

        return ResultSuccess(emprestimo)

    def execute(self, id: int):
        resultado = self.get_emprestimo(id)
        if not resultado:
            return resultado

        try:
            resposta = self.repo.remover_emprestimo(id, self.policy.user)
            return ResultSuccess(resposta)
        except Exception as e:
            return ResultError(f"Erro ao remover empréstimo: {e}")


class GerarTermoResponsabilidadeUsecase:
    def __init__(
        self,
        repo: EmprestimoRepository,
        policy: EmprestimoPolicy,
        service: PDFService,
    ) -> None:
        self.repo = repo
        self.policy = policy
        self.service = service

    def execute(self, emprestimo: EmprestimoEntity):
        if not self.policy.pode_gerar_termos(emprestimo):
            return ResultError("Você não tem permissão para gerar termos.")

        if (
            emprestimo.estado != EmprestimoEstadoEnum.ATIVO
            or emprestimo.data_devolucao is not None
        ):
            return ResultError("Empréstimo já finalizado")
        try:
            resposta = self.service.gerar_termo_responsabilidade(
                emprestimo, self.policy.user
            )
        except Exception as e:
            return ResultError(f"Erro ao gerar PDF: {e}")

        return ResultSuccess(resposta)


class GerarTermoDevolucaoUsecase:
    def __init__(
        self,
        repo: EmprestimoRepository,
        policy: EmprestimoPolicy,
        service: PDFService,
    ) -> None:
        self.repo = repo
        self.policy = policy
        self.service = service

    def execute(self, emprestimo: EmprestimoEntity):
        if not self.policy.pode_gerar_termos(emprestimo):
            return ResultError("Você não tem permissão para gerar termos.")

        if (
            emprestimo.estado != EmprestimoEstadoEnum.FINALIZADO
            or emprestimo.data_devolucao is None
        ):
            return ResultError("Empréstimo não finalizado.")
        try:
            resposta = self.service.gerar_termo_devolucao(emprestimo, self.policy.user)
        except Exception as e:
            return ResultError(f"Erro ao gerar PDF: {e}")

        return ResultSuccess(resposta)


class NotificarDevolucaoUsecase:
    def __init__(
        self,
        emprestimo_repo: EmprestimoRepository,
        aluno_repo: AlunoRepository,
        service: MailService,
    ):
        self.emprestimo_repo = emprestimo_repo
        self.aluno_repo = aluno_repo
        self.service = service

    def execute(self, data_devolucao: date):
        emprestimos = self.emprestimo_repo.listar_emprestimos_devolucao_proxima(
            data_devolucao
        )

        map_sucesso: dict[str, int] = {}

        for e in emprestimos:
            destinatario = self.aluno_repo.buscar_por_id(e.aluno_id).email

            if destinatario not in map_sucesso.keys():
                map_sucesso[destinatario] = 0

            assunto = f"[SIGEMP] - Lembrete: prazo de devolução do bem '{e.bem_descricao} ({e.bem_patrimonio})'"
            mensagem = (
                f"Prezado {e.aluno_nome},\n\n"
                f"A devolução do bem ''{e.bem_descricao} ({e.bem_patrimonio})'' "
                f"deve ser feita no dia {e.data_devolucao_prevista.strftime('%d/%m/%Y')}. "
                f"Não esqueça de assinar o termo de devolução ao realizar a entrega.\n\n"
                f"Atenciosamente,\n Comissão de Empréstimo de Bens Móveis."
            )

            retorno = self.service.enviar_email(
                mensagem, [destinatario], assunto=assunto
            )

            map_sucesso[destinatario] += retorno

        if sum(map_sucesso.values()) == 0:
            return ResultError(
                f"Erro ao notificar: Nenhum e-mail notificado: {map_sucesso.keys()}"
            )
        return ResultSuccess(map_sucesso)
